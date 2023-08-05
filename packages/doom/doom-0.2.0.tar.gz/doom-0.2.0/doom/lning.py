#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Natural logging.  Hah!
"""
import fcntl

from logging.handlers import WatchedFileHandler


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
