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
import shutil
import os
import tempfile
import unittest

from eam.fileutils import makedirs


class TestMakedirs(unittest.TestCase):

    def test_simple(self):
        # Given
        tempdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tempdir)
        path = os.path.join(tempdir, "foo")

        # When
        makedirs(path)

        # Then
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.isdir(path))

        # When
        # calling makedirs on existing directory
        makedirs(path)

        # Then
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.isdir(path))
