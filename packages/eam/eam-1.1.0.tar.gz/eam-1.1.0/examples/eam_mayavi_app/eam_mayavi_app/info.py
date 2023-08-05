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
import os


def info():
    """ Provides information to the "eam" package.

    This function is advertised via a setuptools extension point; it will be
    called by eam to communicate information about the application.  See
    the eam docs for the meaning of the dict keys used below.

    .. note:: Paths should be absolute

    """
    import mayavi
    MAYAVI = os.path.abspath(os.path.dirname(mayavi.__file__))
    icon = os.path.join(MAYAVI, 'images', 'm2.ico')
    return {
        'name': 'mayavi_demo',
        'description': '3D visualization of scientific data in Python',
        'license': 'BSD-like',
        'copyright': '(c) 2008-2018 Enthought',
        'version': '4.5.0',
        'commands': [
            {'name': 'Mayavi2', 'command': 'mayavi2',
             'shortcut': 'desktop', 'icon': icon}]}
