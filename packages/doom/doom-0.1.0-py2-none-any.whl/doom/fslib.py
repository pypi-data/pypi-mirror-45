#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File-system utilities.
"""
import errno
import os
import sys


# TODO: Once py3-only, this can be replaced with
#  just `os.makedirs(path, mode, exists_ok=True)`
def makedirs(path, mode=0o777):
    """
    Patch os.makedirs to set permissions more effectively.

    Apparently os.makedirs doesn't respect the given mode (on some systems)
    if the umask conflicts with it.  So set the umask and then change it
    back.

    https://stackoverflow.com/questions/5231901/
        ... permission-problems-when-creating-a-dir-with-os-makedirs-python

    Parameters
    ----------
    path : str
    mode : octal, default 0o777
    """
    original_umask = os.umask(0)
    try:
        os.makedirs(path, mode=mode)
    except OSError:
        s = sys.exc_info()
        if s[1].errno == errno.EEXIST and os.path.isdir(path):
            # "File exists" error if the directory already exists.
            pass
        else:  # pragma: no cover
            raise
    os.umask(original_umask)
