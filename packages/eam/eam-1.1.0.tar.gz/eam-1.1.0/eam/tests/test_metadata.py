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
import unittest

from ..metadata import Application, Command

COMMAND_METADATA = {
    "name": "hello",
    "command": "eam_example",
    "description": "example",
    "arguments": ["hello"],
    "shortcut": "desktop",
    "schema_version": 1,
    "icon": "path/dummy.ico"}

APPLICATION_METADATA = {
        "copyright": "(c) 2018 Enthought",
        "description": "Some information here",
        "commands": [COMMAND_METADATA],
        "license": "Enthought Proprietary",
        "name": "EAM Example",
        "schema_version": 1,
        "version": "1.0.0"}


class TestMetadata(unittest.TestCase):

    maxDiff = None

    def test_command_roundtrip(self):
        # given
        metadata = COMMAND_METADATA

        # when
        command = Command.from_dict(metadata)
        data = command.to_dict()

        # then
        self.assertEqual(metadata, data)

    def test_application_roundtrip(self):
        # given
        metadata = APPLICATION_METADATA

        # when
        application = Application.from_dict(metadata)
        data = application.to_dict()

        # then
        self.assertEqual(metadata, data)
