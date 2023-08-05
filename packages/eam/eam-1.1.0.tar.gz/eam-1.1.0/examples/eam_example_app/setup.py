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
from setuptools import setup

setup(
    name='eam_example_app',
    version='1.0.1',
    license='Proprietary',
    packages=['eam_example_app'],
    entry_points={
        'enthought_app_metadata': ['example_app = eam_example_app.info:info'],
        'console_scripts': ['example_app = eam_example_app.cli:run']})
