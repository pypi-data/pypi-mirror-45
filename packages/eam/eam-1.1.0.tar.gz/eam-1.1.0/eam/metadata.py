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
from collections import OrderedDict
from json import JSONEncoder
import logging
import os
import sys


import enum

logger = logging.getLogger(__name__)


@enum.unique
class ShortcutType(enum.Enum):
    none = None
    desktop = "desktop"


class WOOrderedDict(OrderedDict):
    """Write once ordered dict.

    An OrderedDict that does not allow item overwrite.

    """

    def __setitem__(self, key, value):
        if key in self:
            message = "Overwriting old key '{}' is not allowed."
            raise ValueError(message.format(key))
        super(WOOrderedDict, self).__setitem__(key, value)


class Command(object):

    SCHEMA_VERSION = 1

    def __init__(
            self, name, command, description,
            arguments=None, icon=None, shortcut=None):
        try:
            shortcut = ShortcutType[shortcut]
        except KeyError:
            shortcut = ShortcutType.none

        #: The name of the command
        self.name = name
        #: The command description, optional.
        self.description = description if description is not None else ""
        #: The command executable.
        self.command = command
        #: The list of command arguments, optional.
        self.arguments = arguments
        #: The type of shortcut to cerate, optional.
        #: Supported options {None, desktop}.
        #: Default is None (no shortcut).
        #: If an invalid option is provided then value is None.
        self.shortcut = shortcut
        #: Icon file to use for the shortcut, optional. Default
        #: is None (use the python executable icon).
        self.icon = icon
        self._schema_version = self.SCHEMA_VERSION

    @classmethod
    def from_dict(cls, data):
        schema_version = data.get('schema_version', None)
        if schema_version is None:
            logger.warn(
                'Could not identify the schema version,'
                ' conversion might fail.')
        elif schema_version > cls.SCHEMA_VERSION:
            logger.warn(
                'Unsupported schema version {},'
                ' conversion might fail'.format(schema_version))
        return cls(
            name=data['name'],
            command=data['command'],
            # description is optional
            description=data.get('description', ''),
            # shortcut is optional
            shortcut=data.get('shortcut', 'none'),
            # arguments is optional
            arguments=data.get('arguments', None),
            # icon is optional
            icon=data.get('icon', None))

    @property
    def executable_path(self):
        prefix = os.path.dirname(sys.executable)
        command = self.command
        if sys.platform.startswith('win'):
            if command.endswith('.exe'):
                return os.path.join(prefix, 'Scripts', command)
            else:
                return os.path.join(prefix, 'Scripts', command + '.exe')
        else:
            return os.path.join(prefix, command)

    def to_dict(self):
        return {
            'schema_version': self.SCHEMA_VERSION,
            'name': self.name,
            'description': self.description,
            'command': self.command,
            'arguments': self.arguments,
            'shortcut': self.shortcut.value,
            'icon': self.icon}


class Application(object):

    SCHEMA_VERSION = 1

    def __init__(
            self, name, description, license, copyright, version, commands):
        #: The name of the application.
        self.name = name
        #: A short summary description.
        self.description = description if description is not None else ""
        #: The application license.
        self.license = license
        #: The copyright owner.
        self.copyright = copyright
        #: The application version
        self.version = version
        #: A write once ordered dictionary of commands.
        #: Note that the first command will be considered the default.
        self.commands = WOOrderedDict()
        for command in commands:
            self.commands[command.name] = command
        #: The max schema version supported.
        self._schema_version = self.SCHEMA_VERSION

    @classmethod
    def from_dict(cls, data):
        schema_version = data.get('schema_version', None)
        if schema_version is None:
            logger.warn(
                'Could not identify the schema version,'
                ' conversion might fail.')
        elif schema_version > cls.SCHEMA_VERSION:
            logger.warn(
                'Unsupported schema version {},'
                ' conversion might fail'.format(schema_version))
        commands = [Command.from_dict(options) for options in data['commands']]
        return cls(
            name=data['name'],
            # description is optional
            description=data.get('description', ''),
            license=data['license'],
            copyright=data['copyright'],
            version=data['version'],
            commands=commands)

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'license': self.license,
            'copyright': self.copyright,
            'version': self.version,
            'schema_version': self._schema_version,
            'commands': [
                self.commands[key].to_dict() for key in self.commands]}


class MetadataJSONEncoder(JSONEncoder):

    def default(self, o):
        try:
            data = o.to_dict()
        except AttributeError:
            return JSONEncoder.default(self, o)
        else:
            return data
