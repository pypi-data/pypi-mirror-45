#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Miscellaneous utilities; in future versions these may be sorted into more
well-scoped files.
"""
import signal
from functools import wraps


def timeout_decorator(timeout, default):
    """
    A function decorated with timeout_decorator(timeout, default) either
    finishes within "timeout" seconds or will exit and return "default".

    timeout=None defaults to an infinite bound.

    Parameters
    ----------
    timeout : int or None
    default : object

    Returns
    -------
    function

    Notes
    -----
    Copied (with some edits) from:
    http://pguides.net/python-tutorial/python-timeout-a-function/

    Examples
    --------
    >>> @timeout_decorator(3, None)
    >>> def urlget(URL):
    >>>      return urllib.urlopen(URL)
    >>>
    >>> page = urlget(URL)  # ... 3 seconds go by ...
    Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
    TimeoutException
    """
    # TODO: Windows version
    # TODO: Version that works in threads, screen

    _validate_timeout(timeout)

    if timeout == 0:
        return lambda func: func

    def timeout_function(f):
        @wraps(f)
        def f2(*args, **kwargs):
            try:
                old_handler = signal.signal(signal.SIGALRM, _timeout_handler)
            except ValueError:
                # ValueError: signal only works in main thread
                #  timeout_decorator does not work when called
                #  within a thread other than the main thread.
                #  ValueError will also be raised on Windows.
                retval = f(*args, **kwargs)
            else:
                signal.setitimer(signal.ITIMER_REAL, timeout)
                # used timer instead of alarm to allow for non-integer timeouts
                #  signal.alarm(int(timeout))
                try:
                    retval = f(*args, **kwargs)
                except TimeoutException:
                    print("TimeoutException")
                    retval = default
                except:  # noqa:E722
                    signal.alarm(0)
                    raise
                finally:
                    signal.signal(signal.SIGALRM, old_handler)
                signal.alarm(0)

            return retval
        return f2

    return timeout_function


def _validate_timeout(timeout):
    msg = ('timeout must be a non-negative number, not {timeout}.'
           .format(timeout=timeout))
    if not isinstance(timeout, (int, float)):  # pragma: no cover
        raise ValueError(timeout, msg)
    elif timeout < 0:  # pragma: no cover
        raise ValueError(timeout, msg)


class TimeoutException(Exception):
    pass


def _timeout_handler(signum, frame):
    raise TimeoutException()
