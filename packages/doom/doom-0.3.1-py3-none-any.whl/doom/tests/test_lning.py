#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import multiprocessing
import random
import re
import string
import tempfile
import threading

import mock
import pytest
from six import unichr
from six.moves import StringIO

from doom.lning import (
    LockingCrossProcessHandler, UniqueFilter, natural_formatter
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


def _gen_names(num_names):
    # manually implementing to avoid hypothesis dependency; with hypothesis
    #  we would just use
    #  @given(st.text(alphabet=string.ascii_letters + string.digits,
    #                 min_size=3, max_size=120))
    names = []

    for n in range(num_names):
        nchars = random.randint(3, 120)
        chars = [random.choice(string.ascii_uppercase + string.digits)
                 for _ in range(nchars)]
        name = ''.join(chars)
        names.append(name)
    return names


def _gen_msgs(num_msgs):
    # manually implementing to avoid hypothesis dependency; with hypothesis
    #  we would just use
    #  @given(st.text(min_size=1, max_size=256))
    msgs = []

    for n in range(num_msgs):
        nchars = random.randint(1, 256)
        # Note: 1000 is an arbitrary upper bound
        points = [random.randint(40, 1000) for _ in range(nchars)]
        chars = [unichr(x) for x in points]
        msg = ''.join(chars)
        msgs.append(msg)
    return msgs


@pytest.mark.parametrize('name', _gen_names(5))
@pytest.mark.parametrize('msg', _gen_msgs(5))
@pytest.mark.parametrize('level', [10, 20, 30, 40, 50])
def test_logformat(level, name, msg):

    if src_filename in name:  # pragma: no cover
        # equiv: assume(src_filename not in name)
        pytest.skip('Test assumption invalid')

    logger = logging.Logger(name)
    # patching.patch_makeRecord(logger)
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
    with mock.patch.object(handler, 'stream', c):
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
