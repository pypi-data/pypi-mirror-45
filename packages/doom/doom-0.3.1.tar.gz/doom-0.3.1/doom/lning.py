#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Natural logging.  Hah!
"""
import fcntl

from logging import Filter, Formatter
from logging.handlers import WatchedFileHandler


# My preferred format for log messsages
natural_logformat = (
    '%(asctime)s.%(msecs)03d - '
    '%(name)-20.20s - %(process)-5d - '
    '%(levelname)-8s - '
    '%(module).23s.%(funcName)s:%(lineno)-4s - '
    '%(message)s'
)
natural_formatter = Formatter(natural_logformat, '%Y-%m-%d %H:%M:%S')
# TODO: %Z for timezone may be worth considering
# TODO: port tests


class LockingCrossProcessHandler(WatchedFileHandler):
    """
    Adds cross-process locking to the stdlib handler, which itself only has
    cross-thread locking.

    Linux/OSX only.
    """
    def acquire(self):
        """Acquire the I/O thread/process lock."""
        if self.lock:
            self.lock.acquire()
        if self.stream is None:
            self.stream = self._open()
        fcntl.flock(self.stream, fcntl.LOCK_EX)

    def release(self):
        """Release the I/O thread/process lock."""
        if self.lock:
            self.lock.release()
        if self.stream:
            fcntl.flock(self.stream, fcntl.LOCK_UN)


class UniqueFilter(Filter):
    def __init__(self):
        self.no_duplicates = set()
        self.handler = None  # TODO: is this needed?

    def add_no_duplicate_msg(self, msg):
        """
        Add a string `msg` to the list of messages that haev already been
        issued and should not be issued again.
        """
        self.no_duplicates.add(msg)

    def filter(self, record):
        msg = record.msg
        if msg in self.no_duplicates:
            return False
        return True
