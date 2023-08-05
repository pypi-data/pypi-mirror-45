#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import tempfile
import os
import threading
import multiprocessing

import pytest

from doom.lning import LockingCrossProcessHandler, UniqueFilter


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
