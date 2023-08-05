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

HERE = os.path.abspath(__file__)


def info():
    """ Provides information to the "eam" package.

    This function is advertised via a setuptools extension point; it will be
    called by eam to communicate information about the application.  See
    the eam docs for the meaning of the dict keys used below.

    .. note:: Paths should be absolute

    """

    icon = os.path.join(HERE, 'data', 'icon.ico')
    return {
        'name': 'EAM Example',
        'description': 'Some information here',
        'license': 'Enthought Proprietary',
        'copyright': '(c) 2018 Enthought',
        'version': u'1.0.1',
        'commands': [
            {'name': 'hello',
             'command': 'example_app',
             'shortcut': 'desktop',
             'icon': icon},
            {'name': 'version',
             'command': 'example_app',
             'arguments': ['--version']}]}
