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
import ctypes
from ctypes.wintypes import DWORD, HANDLE, HWND, INT
from ctypes import HRESULT

from .util import function_factory, LPTSTR, check_hresult

# Use a local copy of the shell32 dll.
shell32 = ctypes.WinDLL('shell32')


SHGetFolderPath = function_factory(
    shell32.SHGetFolderPathW,
    [HWND, INT, HANDLE, DWORD, LPTSTR],
    HRESULT,
    check_hresult)
