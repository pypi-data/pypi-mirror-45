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
import os
import tempfile
import shutil
import sys
import unittest

import mock

from eam.metadata import Command
from eam.shortcuts import (
    create_shortcut, remove_shortcut, has_shortcut)


@unittest.skipIf(
    not sys.platform.startswith('win'),
    "Windows only shortcut tests")
class TestShortcuts(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tempdir)

    def test_create_shortcut(self):
        # given
        import comtypes  # noqa
        from comtypes.client import CreateObject
        from comtypes.shelllink import ShellLink
        from comtypes.persist import IPersistFile
        from eam._win32.constants import STGM_READ
        from ..win import SHORTCUT_FILENAME

        command = Command(
            name='eam-test', description='test',
            arguments=['--version'],
            shortcut='desktop',
            command='eam', icon=None)

        # when
        function_path = 'eam.shortcuts.win._get_windows_folder'
        with mock.patch(function_path, return_value=self.tempdir):
            create_shortcut(command)

        # then
        expected = os.path.join(
            self.tempdir, SHORTCUT_FILENAME.format(command.name))
        self.assertTrue(os.path.exists(expected))
        shortcut = CreateObject(ShellLink)
        persist_file = shortcut.QueryInterface(IPersistFile)
        persist_file.Load(expected, STGM_READ)
        self.assertTrue(shortcut.GetPath().endswith(command.command + '.exe'))
        self.assertEqual(shortcut.GetArguments(), ' '.join(command.arguments))

    def test_remove_shortcut(self):
        # given
        from ..win import SHORTCUT_FILENAME
        command = Command(
            name='eam-test', description='test',
            command='eam', icon=None)
        shortcut = os.path.join(
            self.tempdir, SHORTCUT_FILENAME.format(command.name))
        with open(shortcut, 'w'):
            pass

        # when
        function_path = 'eam.shortcuts.win._get_windows_folder'
        with mock.patch(function_path, return_value=self.tempdir):
            remove_shortcut(command)

        # then
        self.assertFalse(os.path.exists(shortcut))

    def test_has_shortcut(self):
        # given
        from ..win import SHORTCUT_FILENAME
        command = Command(
            name='eam-test', description='test',
            command='eam', icon=None)
        shortcut = os.path.join(
            self.tempdir, SHORTCUT_FILENAME.format(command.name))

        # when
        function_path = 'eam.shortcuts.win._get_windows_folder'
        with mock.patch(function_path, return_value=self.tempdir):
            result = has_shortcut(command)

        # then
        self.assertFalse(result)

        # when
        with open(shortcut, 'w'):
            pass
        with mock.patch(function_path, return_value=self.tempdir):
            result = has_shortcut(command)

        # then
        self.assertTrue(result)
