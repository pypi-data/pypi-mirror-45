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
from __future__ import absolute_import, unicode_literals, print_function
import ctypes
from ctypes.wintypes import MAX_PATH
import os
import sys
import logging

import comtypes  # noqa
from comtypes.client import CreateObject
from comtypes.shelllink import ShellLink
from comtypes.persist import IPersistFile

from eam._win32.shell32 import SHGetFolderPath
from eam._win32.constants import CSIDL_DESKTOP, SHGFP_TYPE_CURRENT


logger = logging.getLogger(__name__)
SHORTCUT_FILENAME = "{}.lnk"


def create_shortcut(command):
    """ Create a shortcut in the desktop folder.

    Parameters
    ----------
    command : Command
        The command for which to create a shortcut.

    """
    shortcut = CreateObject(ShellLink)
    shortcut.SetPath(command.executable_path)
    if command.arguments is not None:
        shortcut.SetArguments(' '.join(command.arguments))
    if command.icon is None:
        shortcut.SetIconLocation(sys.executable, 1)
    else:
        shortcut.SetIconLocation(command.icon, 0)

    filename = SHORTCUT_FILENAME.format(command.name)
    filepath = os.path.join(_get_windows_folder(CSIDL_DESKTOP), filename)
    persist_file = shortcut.QueryInterface(IPersistFile)
    persist_file.Save(filepath, True)

    message = "Shortcut {} was created in the desktop folder"
    logger.info(message.format(filename))


def remove_shortcut(command):
    """ Remove a shortcut from the desktop folder.

    Parameters
    ----------
    command : Command
        The command for which to remove the shortcut.

    """
    filename = SHORTCUT_FILENAME.format(command.name)
    filepath = os.path.join(_get_windows_folder(CSIDL_DESKTOP), filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        message = "Shortcut {} was deleted from the desktop folder"
        logger.info(message.format(filename))
    else:
        message = "Shortcut {} was not found in desktop folder"
        logger.info(message.format(filename))


def has_shortcut(command):
    """ Return the true if there is a shortcut for the command.

    Parameters
    ----------
    command : Command
        The command for which to create a shortcut.

    Returns
    -------
    result : bool
        True if the a shortcut with the expected name exists in
        the desktop.

    """
    filename = SHORTCUT_FILENAME.format(command.name)
    filepath = os.path.join(_get_windows_folder(CSIDL_DESKTOP), filename)
    return os.path.exists(filepath)


def _get_windows_folder(csidl):
    buffer_ = ctypes.create_unicode_buffer(MAX_PATH)
    SHGetFolderPath(0, csidl, 0, SHGFP_TYPE_CURRENT, buffer_)
    return buffer_.value
