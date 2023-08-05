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
import logging
import os
import shutil
import tempfile
import unittest

import testfixtures
from eam import __version__

from eam.logging import enable_logging


class TestLogging(unittest.TestCase):

    def tearDown(self):
        logging.shutdown()

    def test_no_logging(self):
        # when
        with testfixtures.LogCapture() as log:
            with testfixtures.OutputCapture() as output:
                enable_logging(None, None)

        # then
        log.check()
        output.compare()

    def test_output_logging(self):
        # when
        with testfixtures.LogCapture() as log:
            with testfixtures.OutputCapture() as output:
                enable_logging(1, None)

        # then
        log.check()
        expected = 'Using eam version {}'.format(__version__)
        output.compare(expected)

    def test_file_logging(self):
        # given
        tempdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tempdir)
        log_file = os.path.join(tempdir, 'log')

        # when
        with testfixtures.LogCapture() as log:
            with testfixtures.OutputCapture() as output:
                enable_logging(None, log_file)

        # then
        log.check()
        output.compare()
        with open(log_file, 'r') as handle:
            log = handle.readlines()
        self.assertEqual(len(log), 1)
        expected = 'Using eam version {}'.format(__version__)
        self.assertIn(expected, log[0])
