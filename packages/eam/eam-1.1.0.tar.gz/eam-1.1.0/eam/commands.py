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
from collections import OrderedDict
import json
from pkg_resources import iter_entry_points
import subprocess

from .metadata import Application, MetadataJSONEncoder, ShortcutType
from .shortcuts import (
    create_shortcut, remove_shortcut, has_shortcut)


def info_cmd(return_json=False):
    """ Display information on installed apps

    Parameters
    ----------
    return_json : bool
        When set the output is formated as a json string

    """
    applications = _collect_applications()

    if return_json:
        print(
            json.dumps(
                applications,
                cls=MetadataJSONEncoder,
                separators=(',', ':'),
                indent=4,
                sort_keys=True, ))
    else:
        for entry_point_name in sorted(applications):
            application = applications[entry_point_name]
            msg = '{} ({}): {}'.format(
                entry_point_name, application.version, application.name)
            print(msg)


def start_cmd(name=None):
    """ Start the application.

    Parameters
    ----------
    name : string, optional
        The name of the application to start. If not passed then the
        first application that is found in the metadata entry point is
        considered the default application.

    .. note::
       The command to start an application is by default the first
       command in the list of commands.

    """
    application = _select_application(name)
    _, start = application.commands.popitem(last=False)
    arguments = [] if start.arguments is None else start.arguments
    subprocess.check_call([start.command] + arguments)


def remove_cmd(name=None):
    """ Remove the application setup.

    Parameters
    ----------
    name : string, optional
        The name of the application to remove. If not passed then the
        first application that is found in the metadata entry point is
        considered the default application.

    """
    application = _select_application(name)
    remove_shortcuts_cmd(name)
    print("Setup removed for application '{}'.".format(application.name))


def configure_cmd(name=None):
    """ Configure the application for usage.

    Parameters
    ----------
    name : string, optional
        The name of the application to configure. If not passed then the
        first application that is found in the metadata entry point is
        considered the default application.

    """
    application = _select_application(name)
    create_shortcuts_cmd(name)
    print("Application '{}' configured.".format(application.name))


def create_shortcuts_cmd(name=None):
    """ Create shortcuts for an application.

    Parameters
    ----------
    name : string, optional
        The name of the application to create shortcuts for. If not
        passed then the first application that is found in the
        metadata entry point is considered the default application.

    """
    application = _select_application(name)
    print(
        "Creating shortcuts for the '{}' application.".format(
            application.name))
    for key in application.commands:
        command = application.commands[key]
        if command.shortcut == ShortcutType.desktop:
            create_shortcut(command)


def remove_shortcuts_cmd(name=None):
    """ Remove shortcuts for an application.

    Parameters
    ----------
    name : string, optional
        The name of the application to remove shortcuts for. If not
        passed then the first application that is found in the
        metadata entry point is considered the default application.

    """
    application = _select_application(name)
    print(
        "Removing shortcuts for the '{}' application.".format(
            application.name))
    for key in application.commands:
        command = application.commands[key]
        if command.shortcut == ShortcutType.desktop:
            remove_shortcut(command)


def list_shortcuts_cmd(name=None):
    """ List the shortcuts for an application.

    Parameters
    ----------
    name : string, optional
        The name of the application to list shortcuts for. If not
        passed then the first application that is found in the
        metadata entry point is considered the default application.

    """
    application = _select_application(name)
    rows = [(' ', 'Name', 'Shortcut')]
    for key in application.commands:
        command = application.commands[key]
        if has_shortcut(command):
            exists = '*'
        else:
            exists = ' '
        rows.append(
            (exists, command.name, str(command.shortcut.value)))
    _tabulate(rows, header=True)
    print("\nexisting shortcuts are designated with a `*`")


def _collect_applications():
    applications = OrderedDict()
    for entry_point in iter_entry_points('enthought_app_metadata'):
        metadata = entry_point.resolve()()
        applications[entry_point.name] = Application.from_dict(metadata)
    return applications


def _get_default_application():
    _, application = _collect_applications().popitem(last=False)
    return application


def _select_application(name=None):
    if name is None:
        return _get_default_application()
    else:
        return _collect_applications()[name]


def _tabulate(rows, header=False):
    rows_count = len(rows)
    if rows_count == 0:
        return
    columns_count = len(rows[0])
    if columns_count == 0:
        return

    widths = [0] * columns_count
    for row in rows:
        for index, column in enumerate(row):
            length = len(column)
            if widths[index] < length:
                widths[index] = length

    template = "a:{}b " * columns_count
    template = template[:-1].format(*widths)
    template = template.replace("a", "{")
    template = template.replace("b", "}")
    separator = template.replace("{:", "{0:{fill}<")

    for index, row in enumerate(rows):
        if header and index == 1:
            print(separator.format("", fill="-"))
        print(template.format(*row).rstrip())
