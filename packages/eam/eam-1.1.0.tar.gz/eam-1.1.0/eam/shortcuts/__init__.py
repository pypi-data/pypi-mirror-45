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

import logging
import sys


logger = logging.getLogger(__name__)


if sys.platform.startswith('win'):
    from .win import create_shortcut, remove_shortcut, has_shortcut
else:
    def create_shortcut(command):
        logger.info("Shortcut operations not supported for this platform")

    def remove_shortcut(command):
        logger.info("Shortcut operations not supported for this platform")

    def has_shortcut(command):
        logger.info("Shortcut operations not supported for this platform")
        return False
