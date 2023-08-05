#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Natural logging.  Hah!

logging configured with lning has two main features:

- LockingCrossProcessHandler ensures that multiple processes can log to
  the same file without clobbering each other's messages.

- natural_formatter and patch_logger format log output with consistent
  whitespace, which I find more pleasant than the alternative.
"""
import fcntl
import os

from logging import Filter, Formatter, Logger
from logging.handlers import WatchedFileHandler

from six import PY2

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

_make_record = Logger.makeRecord


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


def patch_logger(logger):
    """
    Patch a Logger object to use remakeRecord instead of the stdlib makeRecord.

    Parameters
    ----------
    logger : Logger
    """
    def makeRecord(name, level, fn, lno, msg, args, exc_info,
                   func=None, extra=None, sinfo=None):
        return remakeRecord(logger, name, level, fn, lno,
                            msg, args, exc_info, func,
                            extra, sinfo)

    logger.makeRecord = makeRecord


def remakeRecord(self, name, level, fn, lno, msg, args, exc_info,
                 func=None, extra=None, sinfo=None):
    """
    To get log records with entries that are nicely aligned, we have to
    adjust the records in ways that are not always possible via python's
    string formatting sub-language.

    Record attributes:
        self.args = args
        self.levelname = getLevelName(level)
        self.levelno = level
        self.pathname = pathname
        self.filename = os.path.basename(pathname)
        self.module = os.path.splitext(self.filename)[0]
        self.filename = pathname
        self.module = "Unknown module"
        self.exc_info = exc_info
        self.exc_text = None      # used to cache the traceback text
        self.lineno
        self.funcName
        self.created
        self.msecs
        self.relativeCreated
        self.thread
        self.threadName
        self.process
        self.processName

    Parameters
    ----------
    self : logger
    name : str
    level : int
    fn : str
    lno : int
    msg : str
    args : ??
    exc_info : ??
    func : ??
    extra : ??
    sinfo : ??

    Returns
    -------
    LogRecord
    """
    # TODO: fill in "??" entries in docstring Parameters

    # Truncate the name after 20 characters --> parameterize
    nmax = 20
    name = name[:nmax]
    name = name + ' ' * (nmax - len(name))

    # Note: formatting will break lf lno > 9999
    slno = str(lno)
    slno = slno + ' ' * (4 - len(slno))
    # Because the formatting string pads it to 4 places already,
    #  this ensures that the formatting here does the same.

    module_name = os.path.splitext(os.path.split(fn)[-1])[0]
    mdl = module_name[:30 - 7]
    # truncate module name so as to allow for 7 characters remaining in
    #  a 30 character budget.

    mf = mdl + '.' + str(func)
    mfl = mf + ':' + slno
    nchars = len(mfl)

    # Paramaterize 30
    fmax = 30
    cut_chars = min(0, fmax - nchars)
    pad_chars = max(0, fmax - nchars)

    lno = slno + ' ' * pad_chars
    if cut_chars < 0:
        func = func[:cut_chars]

    if PY2:  # pragma: no cover
        record = _make_record(self, name, level, fn, lno, msg, args,
                              exc_info, func, extra)
    else:  # pragma: no cover
        # Python3 added the "sinfo" kwarg.
        record = _make_record(self, name, level, fn, lno, msg, args,
                              exc_info, func, extra, sinfo)
    return record
