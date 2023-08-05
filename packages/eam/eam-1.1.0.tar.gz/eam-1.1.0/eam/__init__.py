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
from __future__ import absolute_import, unicode_literals

try:
    from eam._version import version as __version__
except ImportError:  # pragma: no cover
    __version__ = 'notset'

import logging


class NullHandler(logging.Handler):  # pragma: no cover
    def emit(self, record):
        pass


logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())
