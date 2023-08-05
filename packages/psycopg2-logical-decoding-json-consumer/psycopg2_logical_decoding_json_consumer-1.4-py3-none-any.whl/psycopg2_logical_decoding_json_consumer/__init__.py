#   Copyright 2019 University of Lancaster
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import heapq
import json
import logging
import select
import time

import psycopg2
import psycopg2.extras

log = logging.getLogger(__name__)

REPLICATION_KEEPALIVE_INTERVAL = 30


class Consumer:
    def __init__(self, transactions_callback, transaction_event_filter=None, max_transactions_gather_count=1, max_transactions_gather_time=None):
        self._transactions_callback = transactions_callback
        self._transaction_event_filter = transaction_event_filter
        self._max_transactions_gather_count = max_transactions_gather_count
        self._max_transactions_gather_time = max_transactions_gather_time

        self._calls = []

        self._replication_keepalive_due_at = None

        self._transactions = []
        self._transactions_process_due_at = None
        self._transaction_events = None

        self._flush_lsn = 0
        self._transactions_flush_lsn = 0

    def call_later(self, delay, callback):
        when = time.monotonic() + delay
        heapq.heappush(self._calls, (when, callback))

    def _maybe_run_call(self):
        if not self._calls:
            return

        if self._calls[0][0] > time.monotonic():
            return

        (due_at, callback) = heapq.heappop(self._calls)

        log.debug("Calling call")
        call_start_time = time.monotonic()
        callback()
        call_time = time.monotonic() - call_start_time
        log.debug("Call done in {:f}s".format(call_time))

    def _advance_flush_lsn(self, new_lsn):
        self._flush_lsn = max(self._flush_lsn, new_lsn)

    def _maybe_send_replication_keepalive(self):
        if self._replication_keepalive_due_at > time.monotonic():
            return

        # If we have no outstanding transactions, and we're not in the process
        # of collecting events within a transaction we can claim to have flushed
        # to the latest message's wal_end.
        # (cursor.wal_end is only available in psycopg2 2.8+).
        if not self._transactions and self._transaction_events is None and hasattr(self._cursor, 'wal_end'):
            self._advance_flush_lsn(self._cursor.wal_end)

        self._send_replication_feedback()

        self._replication_keepalive_due_at = time.monotonic() + REPLICATION_KEEPALIVE_INTERVAL

    def _send_replication_feedback(self):
        flush_lsn_str = lsn_int_to_str(self._flush_lsn)

        log.debug("Sending replication feedback (flushed to lsn {})".format(flush_lsn_str))
        self._cursor.send_feedback(flush_lsn=self._flush_lsn)

    def _maybe_process_transactions(self):
        if not self._transactions:
            return

        process = False

        if self._max_transactions_gather_count is not None:
            if len(self._transactions) >= self._max_transactions_gather_count:
                process = True

        if self._transactions_process_due_at is not None:
            if self._transactions_process_due_at <= time.monotonic():
                process = True

        if not process:
            return

        log.debug("Calling transactions processor")
        call_start_time = time.monotonic()
        self._transactions_callback(self._transactions)
        call_time = time.monotonic() - call_start_time
        log.debug("Transactions processor done in {:f}s".format(call_time))

        self._advance_flush_lsn(self._transactions_flush_lsn)
        self._send_replication_feedback()

        self._transactions = []
        self._transactions_process_due_at = None
        self._replication_keepalive_due_at = time.monotonic() + REPLICATION_KEEPALIVE_INTERVAL

    def _calculate_sleep_time(self):
        next_event_due_at = self._replication_keepalive_due_at

        if self._transactions_process_due_at is not None:
            next_event_due_at = min(next_event_due_at, self._transactions_process_due_at)

        if self._calls:
            next_event_due_at = min(next_event_due_at, self._calls[0][0])

        return next_event_due_at - time.monotonic()

    def _append_transaction(self, replication_message, events):
        if self._transaction_event_filter:
            events = list(filter(self._transaction_event_filter, events))

        self._transactions_flush_lsn = replication_message.wal_end

        # If this transaction contained no events and there are no outstanding
        # transactions we can claim to have flushed to this point.
        if not events:
            if not self._transactions:
                self._advance_flush_lsn(replication_message.wal_end)
            return

        self._transactions.append(events)

        if self._max_transactions_gather_time is not None:
            if self._transactions_process_due_at is None:
                self._transactions_process_due_at = time.monotonic() + self._max_transactions_gather_time

    def connect(self, dsn, slot_name):
        self._connection = psycopg2.connect(
            dsn, connection_factory=psycopg2.extras.LogicalReplicationConnection)
        self._cursor = self._connection.cursor()

        self._cursor.start_replication(slot_name=slot_name, decode=True)

    def run(self):
        self._replication_keepalive_due_at = time.monotonic() + REPLICATION_KEEPALIVE_INTERVAL

        while True:
            replication_message = self._cursor.read_message()

            if replication_message:
                event = json.loads(replication_message.payload)

                if self._transaction_events is None:
                    if event['kind'] == "message":
                        # Message sent with Transactional=False
                        self._append_transaction(replication_message, [event])
                    elif event['kind'] == "begin":
                        self._transaction_events = []
                    else:
                        raise Exception("Message unexpectedly arrived outside of a transaction: {!r}".format(replication_message))

                else:
                    if event['kind'] == "commit":
                        self._append_transaction(replication_message, self._transaction_events)
                        self._transaction_events = None
                    elif event['kind'] == "change":
                        self._transaction_events.append(event)
                    elif event['kind'] == "truncate":
                        self._transaction_events.append(event)
                    elif event['kind'] == "message":
                        self._transaction_events.append(event)
                    else:
                        raise Exception("Message unexpectedly arrived inside a transaction: {!r}".format(replication_message))

            self._maybe_process_transactions()

            # There may be further messages immediately available - treat them
            # with a higher priority than keeping up with calls
            if replication_message:
                continue

            self._maybe_run_call()

            self._maybe_send_replication_keepalive()

            sleep_time = self._calculate_sleep_time()

            if sleep_time > 0:
                log.debug("Sleeping {:f}s".format(sleep_time))
                select.select([self._cursor], [], [], sleep_time)


# LSNs are 64 bit integers but sometimes represented as XXXXXXXX/XXXXXXXX
def lsn_str_to_int(lsn):
    split_lsn = lsn.split("/", 1)
    lsn_high = int(split_lsn[0], 16)
    lsn_low = int(split_lsn[1], 16)

    return (lsn_high << 32) + lsn_low


def lsn_int_to_str(lsn):
    lsn_high = (lsn >> 32) & 0xffffffff
    lsn_low = lsn & 0xffffffff

    return "{:X}/{:X}".format(lsn_high, lsn_low)
