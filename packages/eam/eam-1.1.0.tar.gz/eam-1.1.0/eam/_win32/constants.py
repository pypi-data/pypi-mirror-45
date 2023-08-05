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
from ctypes.wintypes import DWORD, INT

#: The virtual folder that represents the Windows desktop.
CSIDL_DESKTOP = INT(0)

#: The file system directory that contains the user's program groups
#: (which are themselves file system directories). A typical path is
#: C:\Users\IEUser\AppData\Roaming\Microsoft\Windows\Start Menu\Programs
CSIDL_PROGRAMS = INT(2)

#: Indicates that the object is read-only.
STGM_READ = DWORD(0)

#: Retrieve the folder's current path (as opposed to default path).
SHGFP_TYPE_CURRENT = DWORD(0)
