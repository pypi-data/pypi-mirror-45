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


def get_name_length_limit(dirname):
    """
    Find the limit on name lengths associated with the filesystem mount
    containing dirname.

    Parameters
    ----------
    dirname : str

    Returns
    -------
    limit : int
    """
    # TODO: what if we are looking at a symlink?  Do we need the limit for
    #  the source or the target of the link?  The minimum of the two limits?
    dirname = os.path.abspath(dirname)
    while not os.path.exists(dirname):
        # e.g. we passed a file that hasn't been written yet
        dirname = os.path.split(dirname)[0]
    return os.statvfs(dirname).f_namemax
