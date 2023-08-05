#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import tempfile
import os
import threading
import multiprocessing

import pytest

from doom.lning import LockingCrossProcessHandler, UniqueFilter


def _log(logger, msg):
    logger.info(msg)


@pytest.mark.parametrize('parallel_cls', [threading.Thread,
                                          multiprocessing.Process])
def test_LockingCrossProcessHandler(parallel_cls):
    with tempfile.NamedTemporaryFile() as fd:
        path = fd.name

        logger1 = logging.Logger('1')
        handler1 = LockingCrossProcessHandler(path, mode='a', delay=True)
        logger1.addHandler(handler1)

        logger2 = logging.Logger('2')
        handler2 = LockingCrossProcessHandler(path, mode='a', delay=True)
        logger2.addHandler(handler2)

        track1 = parallel_cls(target=_log, args=(logger1, '1' * 1000,))
        track2 = parallel_cls(target=_log, args=(logger2, '2' * 1000,))

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
