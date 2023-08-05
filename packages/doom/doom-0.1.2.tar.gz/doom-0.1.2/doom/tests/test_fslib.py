#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tempfile
import os

from doom.fslib import makedirs


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
