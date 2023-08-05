#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
import signal
import threading

from doom.utils import timeout_decorator


def tfunc(n):
    time.sleep(n)
    return n


tfunc2 = timeout_decorator(1, 'belize')(tfunc)


def test_timeout_decorator():
    tic = time.time()
    ret = tfunc2(10)
    dt = time.time() - tic
    assert ret == 'belize', ret
    assert dt < 1.1, dt
    # Should be barely over .1


def test_timeout_decorator_zero():
    tfunc3 = timeout_decorator(0, 'belize')(tfunc)
    assert tfunc3 is tfunc, (tfunc3, tfunc,)


def test_timeout_decorator_float():
    tfunc4 = timeout_decorator(.1, 'belize')(tfunc)
    tic = time.time()
    tfunc4(10)
    dt = time.time() - tic
    assert dt < .11, dt


def test_timeout_decorator_raises():
    orig_sig = signal.getsignal(signal.SIGALRM)
    s = None
    ret = None
    try:
        ret = tfunc2('foo')
    except Exception:
        s = sys.exc_info()

    assert ret is None, (ret, s,)
    assert isinstance(s[1], TypeError), (ret, s,)
    new_sig = signal.getsignal(signal.SIGALRM)
    assert new_sig == orig_sig, (new_sig, orig_sig,)


def test_timeout_decorator_thread():
    # timeout_decorator did not cut the function off at 1 seconds because it
    # was in a thread.
    tic = time.time()
    th = threading.Thread(target=tfunc2, args=(1.5,))
    th.start()
    th.join()
    dt = time.time() - tic
    assert dt >= 1.5, dt
