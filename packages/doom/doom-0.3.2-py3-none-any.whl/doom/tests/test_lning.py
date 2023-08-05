#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import multiprocessing
import re
import string
import tempfile
import threading

import pytest
from six.moves import StringIO

import hypothesis.strategies as st
from hypothesis import given, assume

from doom.lning import (
    LockingCrossProcessHandler, UniqueFilter, natural_formatter, patch_logger
)

src_filename = os.path.splitext(os.path.split(__file__)[-1])[0]


def _do_log(path, name, msg):
    logger = logging.Logger(name)
    handler = LockingCrossProcessHandler(path, mode='a', delay=True)
    logger.addHandler(handler)

    logger.info(msg)


@pytest.mark.parametrize('parallel_cls', [threading.Thread,
                                          multiprocessing.Process])
def test_LockingCrossProcessHandler(parallel_cls):
    with tempfile.NamedTemporaryFile() as fd:
        path = fd.name

        track1 = parallel_cls(target=_do_log, args=(path, '1', '1' * 1000))
        track2 = parallel_cls(target=_do_log, args=(path, '2', '2' * 1000))

        track1.start()
        track2.start()
        track1.join()
        track2.join()

        with open(path, 'r') as fd:
            content = fd.read()

        # Check that all content get written and none if it got interleaved
        assert '1' * 1000 in content, content
        assert '2' * 1000 in content, content
        assert '121' not in content, content
        assert '212' not in content, content
        # TODO: check that this *doesnt* work with the stdlib handlers,
        #  i.e. LockingCrossProcessHandler isnt pointless.

    assert not os.path.exists(path), path


def test_unique_filter():
    logger = logging.Logger(__name__)
    msg = 'msg'
    record = logger.makeRecord('name', logging.INFO,
                               'test_logFilter', 111, msg, (), exc_info=False)

    filt = UniqueFilter()

    ans = msg in filt.no_duplicates
    assert ans is False, ans

    ret = filt.filter(record)
    assert ret is True, ret

    filt.add_no_duplicate_msg(msg)

    ret = filt.filter(record)
    assert ret is False, ret

    # TODO: test that the message is not emitted?


@given(name=st.text(alphabet=string.ascii_letters + string.digits,
                    min_size=3, max_size=120),
       msg=st.text(min_size=1, max_size=256))
@pytest.mark.parametrize('level', [10, 20, 30, 40, 50])
def test_logformat(level, name, msg):

    if src_filename in name:  # pragma: no cover
        # equiv: assume(src_filename not in name)
        pytest.skip('Test assumption invalid')

    logger = logging.Logger(name)
    # patch_logger(logger)  # optional, but not necessary for this test
    handler = logging.StreamHandler()
    handler.setFormatter(natural_formatter)
    logger.addHandler(handler)

    funcdict = {
        'INFO': logger.info,
        'WARNING': logger.warning,
        'DEBUG': logger.debug,
        'ERROR': logger.error,
        'CRITICAL': logger.critical,
        10: logger.debug,
        20: logger.info,
        30: logger.warning,
        40: logger.error,
        50: logger.critical
    }
    func = funcdict[level]

    c = StringIO()
    handler.stream = c
    func(msg)

    cv = c.getvalue()

    assert re.search(r'^\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} - ', cv)

    name20 = name[:20]
    cvn = cv.find(name20)
    assert cvn == 26, (name, cvn, cv,)

    pid = os.getpid()
    cvp = cv.find(str(pid))
    assert cvp == 49, (str(pid), cvp, cv,)

    cvf = cv.find(src_filename)
    assert cvf == 68, (cvf, cv,)


@given(st.sampled_from([10, 20, 30, 40, 50]),
       st.text(alphabet=string.ascii_letters + '/', min_size=2, max_size=255),
       st.integers(min_value=0, max_value=9999),
       st.text(alphabet=string.ascii_letters + string.digits,
               min_size=3, max_size=120),
       st.text(alphabet=string.ascii_letters + string.digits,
               min_size=1, max_size=256),
       # TODO: generalize to allow binary characters
       st.text(alphabet=string.ascii_letters + string.digits,
               min_size=3, max_size=32))
def test_remake_record(level, fn, lno, name, msg, func):

    module_name = os.path.splitext(os.path.split(fn)[-1])[0]
    assume(module_name != '')
    assume(src_filename not in name)
    assume(func != '')

    logger = logging.Logger(name)
    patch_logger(logger)
    handler = logging.StreamHandler()
    handler.setFormatter(natural_formatter)
    logger.addHandler(handler)

    args = ()
    exc_info = False

    record = logger.makeRecord(name, level, fn, lno, msg, args, exc_info, func)

    c = StringIO()
    handler.stream = c
    logger.handle(record)

    cv = c.getvalue()

    assert re.search(r'^\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} - ', cv)

    tail = cv[26:]
    name20 = name[:20]
    name20 = name20 + ' ' * (20 - len(name20))
    assert tail.startswith(name20), (tail, name20, cv,)

    tail = cv[49:]
    pid = os.getpid()
    spid = str(pid)
    assert tail.startswith(spid), (tail, spid, cv,)

    tail = cv[57:]
    levelname = logging.getLevelName(level)
    assert tail.startswith(levelname), (tail, cv,)

    assert cv[65:68] == ' - ', (cv[65:68], cv,)

    tail = cv[68:]
    split_tail = tail.split(':')[0]
    # This should be module_name.func_name, unless truncated, in which
    #  case it should be the beginning of module_name.func_name
    mdl = module_name[:30 - 7]
    expected = mdl + '.' + func
    assert expected.startswith(split_tail), (expected, split_tail, cv,)
    mfl = split_tail + ':' + str(lno)
    assert tail.startswith(mfl), (mfl, tail, cv,)

    x9 = 98
    cv9x = cv[x9:x9 + 3]
    assert cv9x == ' - ', (cv9x, cv,)

    assert cv.endswith(msg + '\n'), (cv, msg,)
