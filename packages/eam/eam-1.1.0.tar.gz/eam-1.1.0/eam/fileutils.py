#
#  Copyright (c) 2018, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#  Code copied from EDM
from __future__ import absolute_import

import errno
import os
import sys


def _py3_makedirs(name, mode=0o777, exist_ok=False):
    """ Ported from Python 3
    makedirs(name [, mode=0o777][, exist_ok=False])
    Super-mkdir; create a leaf directory and all intermediate ones.  Works like
    mkdir, except that any intermediate path segment (not just the rightmost)
    will be created if it does not exist. If the target directory already
    exists, raise an OSError if exist_ok is False. Otherwise no exception is
    raised.  This is recursive.
    """
    head, tail = os.path.split(name)
    if not tail:
        head, tail = os.path.split(head)
    if head and tail and not os.path.exists(head):
        try:
            _py3_makedirs(head, mode, exist_ok)
        except OSError as e:
            if e.errno == errno.EEXIST:
                # Defeats race condition when another thread created the path
                pass
        cdir = os.curdir
        if isinstance(tail, bytes):
            cdir = bytes(os.curdir).encode('ASCII')
        if tail == cdir:           # xxx/newdir/. exists if xxx/newdir exists
            return
    try:
        os.mkdir(name, mode)
    except OSError:
        # Cannot rely on checking for EEXIST, since the operating system
        # could give priority to other errors like EACCES or EROFS
        if not exist_ok or not os.path.isdir(name):
            raise


if sys.version_info < (3, 3):
    OS_MAKEDIRS = _py3_makedirs
else:
    OS_MAKEDIRS = os.makedirs


def makedirs(path):
    """Recursive directory creation function that does not fail if the
    directory already exists. As of Python 3.3, an exist_ok kwarg has been
    added to os.makedirs.
    """
    OS_MAKEDIRS(path, exist_ok=True)
