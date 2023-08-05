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

import argparse

from . import __version__
from .commands import (
    info_cmd, start_cmd, remove_cmd, configure_cmd,
    create_shortcuts_cmd, remove_shortcuts_cmd, list_shortcuts_cmd)
from .logging import enable_logging


def info_subcommand(subparsers):
    info_parser = subparsers.add_parser(
        "info", description=u"Display information on installed apps")
    info_parser.add_argument(
        "--json",  action=u"store_true",
        help=u"Produce full app information, in JSON format")
    info_parser.set_defaults(command=lambda x: info_cmd(x.json))


def start_subcommand(subparsers):
    start_parser = subparsers.add_parser(
        u"start", description=u"Start a registered application")
    start_parser.add_argument(
        u"--name",  help=u"The name of the application to start.")
    start_parser.set_defaults(
        command=lambda x: start_cmd(name=getattr(x, 'name', None)))


def configure_subcommand(subparsers):
    configure_parser = subparsers.add_parser(
        u"configure", description=u"Configure a registered application")
    configure_parser.add_argument(
        u"--name",  help=u"The name of the application to configure.")
    configure_parser.set_defaults(
        command=lambda x: configure_cmd(name=getattr(x, 'name', None)))


def remove_subcommand(subparsers):
    remove_parser = subparsers.add_parser(
        u"remove", description=u"Remove setup for a registered application")
    remove_parser.add_argument(
        u"--name",  help=u"The name of the application to remove the setup.")
    remove_parser.set_defaults(
        command=lambda x: remove_cmd(name=getattr(x, 'name', None)))


def shortcut_command_group(subparsers):
    shortcut_parser = subparsers.add_parser(
        u"shortcut",
        description=u"Shortcut operations for a registered application")
    shortcut_subparsers = shortcut_parser.add_subparsers(
        title='shortcut subcommands', description='valid subcommands',
        help='additional help')

    # create subcommand
    create_parser = shortcut_subparsers.add_parser(
        u"create",
        description=u"Create shortcuts for a registered application")
    create_parser.add_argument(
        u"--name",  help=u"The name of the application to create shortcuts.")
    create_parser.set_defaults(
        command=lambda x: create_shortcuts_cmd(name=getattr(x, 'name', None)))

    # remove subcommand
    remove_parser = shortcut_subparsers.add_parser(
        u"remove",
        description=u"Remove shortcuts of a registered application")
    remove_parser.add_argument(
        u"--name",  help=u"The name of the application to remove shortcuts.")
    remove_parser.set_defaults(
        command=lambda x: remove_shortcuts_cmd(name=getattr(x, 'name', None)))

    # remove subcommand
    list_parser = shortcut_subparsers.add_parser(
        u"list",
        description=u"List shortcuts of a registered application")
    list_parser.add_argument(
        u"--name",  help=u"The name of the application to apply the setup.")
    list_parser.set_defaults(
        command=lambda x: list_shortcuts_cmd(name=getattr(x, 'name', None)))


def parser_factory():
    parser = argparse.ArgumentParser(
        description=u"Enthought application setup tool",
        prog=u"eam")
    parser.add_argument(
        "-V", "--version", action="store_true",
        help="show program's version number and exit")
    parser.add_argument(
        "-v", "--verbose", action="count", help="Verbosity level")
    parser.add_argument(
        "--log-file",
        help="Filename to use for logging (nothing gets written by default)"),
    subparsers = parser.add_subparsers(
        title='subcommands', description='valid subcommands',
        help='additional help')

    # subcommands
    info_subcommand(subparsers)
    start_subcommand(subparsers)
    configure_subcommand(subparsers)
    remove_subcommand(subparsers)

    # command groups
    shortcut_command_group(subparsers)

    return parser


def cli(argv=None):
    parser = parser_factory()
    args = parser.parse_args(argv)
    if vars(args) == {'verbose': None, 'log_file': None, 'version': False}:
        # no arguments
        parser.print_help()
    elif getattr(args, "version", False):
        print("eam ({})".format(__version__))
    elif hasattr(args, "command"):
        enable_logging(args.verbose, args.log_file)
        args.command(args)
