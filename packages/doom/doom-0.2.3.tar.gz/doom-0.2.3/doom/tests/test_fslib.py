#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tempfile
import os

from doom.fslib import makedirs, get_name_length_limit


def test_makedirs_exists():
    # TODO: when py3 only, use TemporaryDirectory context
    dname = tempfile.mkdtemp()
    ret = makedirs(dname)  # try to make a directory that already exists
    assert ret is None, ret
    os.rmdir(dname)


def test_makedirs_perms():
    dname = tempfile.mkdtemp()
    os.rmdir(dname)
    makedirs(dname)  # Permissions should default to 777
    assert os.path.exists(dname)
    perms = oct(os.stat(dname).st_mode)
    assert perms[-3:] == '777', perms
    os.rmdir(dname)


def test_get_name_length_limit():
    # Largely a smoke test, assumes that os.statvfs(dirname).f_namemax does
    #  what the stdlib docs say
    dirname = os.path.split(__file__)[0]

    result = get_name_length_limit(dirname)
    expected = os.statvfs(dirname).f_namemax
    assert result == expected
    assert isinstance(result, int) and result >= len(dirname)


def test_get_name_length_limit_nonexistent():
    # os.statvfs(dirname) will raise if we pass a non-existent path,
    #  check that we can do this and get the result for the enclosing directory
    dirname = os.path.split(__file__)[0]
    path = os.path.join(dirname, 'non-existent-path')
    assert not os.path.exists(path)
    result = get_name_length_limit(path)
    expected = get_name_length_limit(dirname)
    assert result == expected

    path = os.path.join(path, 'another-level')
    result = get_name_length_limit(path)
    assert result == expected
