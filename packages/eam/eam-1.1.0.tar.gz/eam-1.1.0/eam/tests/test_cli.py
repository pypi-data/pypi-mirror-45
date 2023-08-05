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
import sys
import textwrap
import unittest

import mock
import testfixtures

from eam.cli import cli


class TestCLI(unittest.TestCase):

    @unittest.skipIf(
        sys.version_info.major == 2,
        "Python 2 does not support this functionality")
    def test_no_command(self):
        # given
        command = []

        # when
        with testfixtures.OutputCapture() as output:
            cli(command)

        # then
        expected = textwrap.dedent("""
            usage: eam [-h] [-V] [-v] [--log-file LOG_FILE]
                       {info,start,configure,remove,shortcut} ...

            Enthought application setup tool

            optional arguments:
              -h, --help            show this help message and exit
              -V, --version         show program's version number and exit
              -v, --verbose         Verbosity level
              --log-file LOG_FILE   Filename to use for logging (nothing gets written by
                                    default)

            subcommands:
              valid subcommands

              {info,start,configure,remove,shortcut}
                                    additional help""")  # noqa
        output.compare(expected)

    def test_info_command(self):
        # given
        command = ['info', '--json']

        # when
        with mock.patch('eam.cli.info_cmd') as cmd:
            cli(command)

        # then
        cmd.assert_called_with(True)

    def test_version_option(self):
        # given
        command = ['--version', 'info', '--json']

        # when
        with testfixtures.OutputCapture():
            with mock.patch('eam.cli.info_cmd') as cmd:
                cli(command)

        # then
        cmd.assert_not_called()

    def test_start_command(self):
        # given
        command = ['start']
        command_with_name = ['start', '--name', 'my_application']

        # when
        with mock.patch('eam.cli.start_cmd') as cmd:
            cli(command)

        # then
        cmd.assert_called_with(name=None)

        # when
        with mock.patch('eam.cli.start_cmd') as cmd:
            cli(command_with_name)

        # then
        cmd.assert_called_with(name='my_application')

    def test_configure_command(self):
        # given
        command = ['configure']
        command_with_name = ['configure', '--name', 'my_application']

        # when
        with mock.patch('eam.cli.configure_cmd') as cmd:
            cli(command)

        # then
        cmd.assert_called_with(name=None)

        # when
        with mock.patch('eam.cli.configure_cmd') as cmd:
            cli(command_with_name)

        # then
        cmd.assert_called_with(name='my_application')

    def test_remove_command(self):
        # given
        command = ['remove']
        command_with_name = ['remove', '--name', 'my_application']

        # when
        with mock.patch('eam.cli.remove_cmd') as cmd:
            cli(command)

        # then
        cmd.assert_called_with(name=None)

        # when
        with mock.patch('eam.cli.remove_cmd') as cmd:
            cli(command_with_name)

        # then
        cmd.assert_called_with(name='my_application')


class TestShortcutCLIGroup(unittest.TestCase):

    def test_create_shortcuts(self):
        # given
        command = ['shortcut', 'create']
        command_with_name = ['shortcut', 'create', '--name', 'my_application']

        # when
        with mock.patch('eam.cli.create_shortcuts_cmd') as cmd:
            cli(command)

        # then
        cmd.assert_called_with(name=None)

        # when
        with mock.patch('eam.cli.create_shortcuts_cmd') as cmd:
            cli(command_with_name)

        # then
        cmd.assert_called_with(name='my_application')

    def test_remove_shortcuts(self):
        # given
        command = ['shortcut', 'remove']
        command_with_name = ['shortcut', 'remove', '--name', 'my_application']

        # when
        with mock.patch('eam.cli.remove_shortcuts_cmd') as cmd:
            cli(command)

        # then
        cmd.assert_called_with(name=None)

        # when
        with mock.patch('eam.cli.remove_shortcuts_cmd') as cmd:
            cli(command_with_name)

        # then
        cmd.assert_called_with(name='my_application')

    def test_list_shortcuts(self):
        # given
        command = ['shortcut', 'list']
        command_with_name = ['shortcut', 'list', '--name', 'my_application']

        # when
        with mock.patch('eam.cli.list_shortcuts_cmd') as cmd:
            cli(command)

        # then
        cmd.assert_called_with(name=None)

        # when
        with mock.patch('eam.cli.list_shortcuts_cmd') as cmd:
            cli(command_with_name)

        # then
        cmd.assert_called_with(name='my_application')
