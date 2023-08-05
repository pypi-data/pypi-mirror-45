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
import json
import textwrap
import unittest
from pkg_resources import iter_entry_points

import mock
import testfixtures

from eam.commands import (
    info_cmd, start_cmd, configure_cmd, remove_cmd,
    create_shortcuts_cmd, remove_shortcuts_cmd, list_shortcuts_cmd,
    _select_application, _collect_applications)
from eam.metadata import Command, Application


def get_first_entry_point():
    entry_point = next(iter_entry_points('enthought_app_metadata'))
    metadata = entry_point.resolve()()
    return entry_point.name, Application.from_dict(metadata)


class TestInfo(unittest.TestCase):

    maxDiff = None

    def test_default_behaviour(self):
        # Given
        applications = _collect_applications()

        # When
        with testfixtures.OutputCapture() as output:
            info_cmd()

        # Then
        expected = [
            "{} ({}): {}\n".format(
                application,
                applications[application].version,
                applications[application].name)
            for application in sorted(applications)]
        output.compare(''.join(expected))

    def test_json_output(self):
        # Given
        applications = _collect_applications()

        # When
        with testfixtures.OutputCapture() as output:
            info_cmd(return_json=True)

        # Then
        result = json.loads(output.captured)
        self.assertEqual(len(result), len(applications))
        for key in result:
            self.assertEqual(result[key], applications[key].to_dict())


class TestStart(unittest.TestCase):

    def test_start_default_application(self):
        # Given
        entry_point, application = get_first_entry_point()

        # When
        with mock.patch('subprocess.check_call') as check_call:
            start_cmd()

        # Then
        _, command = application.commands.popitem(last=False)
        arguments = [] if command.arguments is None else command.arguments
        check_call.assert_called_with([command.command] + arguments)

    def test_start_a_application(self):
        # When
        with mock.patch('subprocess.check_call') as check_call:
            start_cmd(name='example_app')

        # Then
        check_call.assert_called_with(['example_app'])

    def test_start_on_command_arguments(self):
        # Given
        application = _select_application('example_app')
        # remove the default command
        application.commands.popitem(last=False)

        # When
        with mock.patch(
                'eam.commands._select_application',
                return_value=application):
            with mock.patch('subprocess.check_call') as check_call:
                start_cmd()

        # Then
        check_call.assert_called_with(['example_app', '--version'])

    def test_start_a_missing_application(self):
        # When
        with mock.patch('subprocess.check_call') as check_call:
            with self.assertRaises(KeyError):
                start_cmd(name='example')

        # Then
        check_call.assert_not_called()


class TestConfigure(unittest.TestCase):

    def test_configure_default_application(self):
        # Given
        entry_point, application = get_first_entry_point()
        shortcut_commands = [
            application.commands[item] for item in application.commands
            if application.commands[item].shortcut.value is not None]

        # When
        with testfixtures.OutputCapture() as output:
            with mock.patch(
                    'eam.commands.create_shortcut') as mocked:
                configure_cmd()

        # Then
        expected = textwrap.dedent("""
            Creating shortcuts for the '{0}' application.
            Application '{0}' configured.""")
        output.compare(expected.format(application.name))
        self.assertEqual(mocked.call_count, 1)
        call = mocked.call_args_list[0]
        self.assertEqual(len(call[0]), len(shortcut_commands))
        command = call[0][0]
        self.assertIsInstance(command, Command)
        self.assertEqual(command.name, shortcut_commands[0].name)

    def test_configure_a_default_application(self):
        # When
        with testfixtures.OutputCapture() as output:
            with mock.patch(
                    'eam.commands.create_shortcut') as mocked:
                configure_cmd('example_app')

        # Then
        expected = textwrap.dedent("""
            Creating shortcuts for the 'EAM Example' application.
            Application 'EAM Example' configured.""")
        output.compare(expected)
        self.assertEqual(mocked.call_count, 1)
        call = mocked.call_args_list[0]
        self.assertEqual(len(call[0]), 1)
        command = call[0][0]
        self.assertIsInstance(command, Command)
        self.assertEqual(command.name, 'hello')


class TestRemove(unittest.TestCase):

    def test_remove_default_application(self):
        # Given
        entry_point, application = get_first_entry_point()
        shortcut_commands = [
            application.commands[item] for item in application.commands
            if application.commands[item].shortcut.value is not None]

        # When
        with testfixtures.OutputCapture() as output:
            with mock.patch(
                    'eam.commands.remove_shortcut') as mocked:
                remove_cmd()

        # Then
        expected = textwrap.dedent("""
            Removing shortcuts for the '{0}' application.
            Setup removed for application '{0}'.""")
        output.compare(expected.format(application.name))
        self.assertEqual(mocked.call_count, 1)
        call = mocked.call_args_list[0]
        self.assertEqual(len(call[0]), len(shortcut_commands))
        command = call[0][0]
        self.assertIsInstance(command, Command)
        self.assertEqual(command.name, shortcut_commands[0].name)

    def test_remove_a_application(self):
        # When
        with testfixtures.OutputCapture() as output:
            with mock.patch(
                    'eam.commands.remove_shortcut') as mocked:
                remove_cmd('example_app')

        # Then
        expected = textwrap.dedent("""
            Removing shortcuts for the 'EAM Example' application.
            Setup removed for application 'EAM Example'.""")
        output.compare(expected)
        self.assertEqual(mocked.call_count, 1)
        call = mocked.call_args_list[0]
        self.assertEqual(len(call[0]), 1)
        command = call[0][0]
        self.assertIsInstance(command, Command)
        self.assertEqual(command.name, 'hello')


class TestShortcut(unittest.TestCase):

    def test_create_shortcuts_cmd(self):
        # given
        function_path = 'eam.commands.create_shortcut'

        # When
        with testfixtures.OutputCapture() as output:
            with mock.patch(function_path) as mocked:
                create_shortcuts_cmd('example_app')

        # Then
        expected = "Creating shortcuts for the 'EAM Example' application."
        output.compare(expected)
        self.assertEqual(mocked.call_count, 1)
        call = mocked.call_args_list[0]
        self.assertEqual(len(call[0]), 1)
        command = call[0][0]
        self.assertIsInstance(command, Command)
        self.assertEqual(command.name, 'hello')

        # When
        with testfixtures.OutputCapture() as output:
            with mock.patch(function_path) as mocked:
                create_shortcuts_cmd('example_app')

        # Then
        output.compare(expected)
        self.assertEqual(mocked.call_count, 1)
        call = mocked.call_args_list[0]
        self.assertEqual(len(call[0]), 1)
        command = call[0][0]
        self.assertIsInstance(command, Command)
        self.assertEqual(command.name, 'hello')

    def test_remove_shortcuts_cmd(self):
        # given
        function_path = 'eam.commands.remove_shortcut'
        entry_point, application = get_first_entry_point()
        shortcut_commands = [
            application.commands[item] for item in application.commands
            if application.commands[item].shortcut.value is not None]

        # When
        with testfixtures.OutputCapture() as output:
            with mock.patch(function_path) as mocked:
                remove_shortcuts_cmd()

        # Then
        expected = "Removing shortcuts for the '{}' application.".format(
            application.name)
        output.compare(expected)
        self.assertEqual(mocked.call_count, 1)
        call = mocked.call_args_list[0]
        self.assertEqual(len(call[0]), len(shortcut_commands))
        command = call[0][0]
        self.assertIsInstance(command, Command)
        self.assertEqual(command.name, shortcut_commands[0].name)

        # When
        with testfixtures.OutputCapture() as output:
            with mock.patch(function_path) as mocked:
                remove_shortcuts_cmd('example_app')

        # Then
        expected = "Removing shortcuts for the 'EAM Example' application."
        output.compare(expected)
        self.assertEqual(mocked.call_count, 1)
        call = mocked.call_args_list[0]
        self.assertEqual(len(call[0]), 1)
        command = call[0][0]
        self.assertIsInstance(command, Command)
        self.assertEqual(command.name, 'hello')

    def test_list_shortcuts_cmd(self):
        # When
        with testfixtures.OutputCapture() as output:
            list_shortcuts_cmd('example_app')

        # Then
        expected = textwrap.dedent("""
              Name    Shortcut
            - ------- --------
              hello   desktop
              version None

            existing shortcuts are designated with a `*`""")
        output.compare(expected)

        # When
        with testfixtures.OutputCapture() as output:
            list_shortcuts_cmd('example_app')

        # Then
        output.compare(expected)
