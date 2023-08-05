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


def run():
    parser = argparse.ArgumentParser(
        description=u"eam example application",
        prog=u"example_app")
    parser.add_argument(u"--version",  action=u"store_true")
    args = parser.parse_args()
    if args.version:
        print("1.0.0")
    else:
        print("hello")
