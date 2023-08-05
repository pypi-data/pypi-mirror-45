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
from __future__ import absolute_import, division, print_function

import os
import subprocess
from setuptools import setup, find_packages

MAJOR = 1
MINOR = 1
MICRO = 0

IS_RELEASED = True

VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)


# Return the git revision as a string
def git_version():
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, env=env,
        ).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        git_revision = out.strip().decode('ascii')
    except OSError:
        git_revision = "Unknown"

    try:
        out = _minimal_ext_cmd(['git', 'rev-list', '--count', 'HEAD'])
        git_count = out.strip().decode('ascii')
    except OSError:
        git_count = '0'

    return git_revision, git_count


def write_version_py(filename='eam/_version.py'):
    template = """\
# -*- coding: utf-8 -*-
#
# Entought product code
#
# (C) Copyright 2018 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is confidential and NOT open source.  Do not distribute.
#
from __future__ import absolute_import, unicode_literals

# THIS FILE IS GENERATED FROM SETUP.PY
version = '{version}'
full_version = '{full_version}'
git_revision = '{git_revision}'
is_released = {is_released}

if not is_released:
    version = full_version
"""
    fullversion = VERSION
    if os.path.exists('.git'):
        git_rev, dev_num = git_version()
    elif os.path.exists('eam/_version.py'):
        # must be a source distribution, use existing version file
        try:
            from eam._version import git_revision as git_rev
            from eam._version import full_version as full_v
        except ImportError:
            raise ImportError("Unable to import git_revision. Try removing "
                              "eam/_version.py and the build "
                              "directory before building.")
        import re
        match = re.match(r'.*?\.dev(?P<dev_num>\d+)\+.*', full_v)
        if match is None:
            dev_num = '0'
        else:
            dev_num = match.group('dev_num')
    else:
        git_rev = "Unknown"
        dev_num = '0'

    if not IS_RELEASED:
        fullversion += '.dev{0}'.format(dev_num)

    with open(filename, "wt") as fp:
        fp.write(template.format(
            version=VERSION,
            full_version=fullversion,
            git_revision=git_rev,
            is_released=IS_RELEASED))


if __name__ == "__main__":
    write_version_py()
    from eam import __version__
    setup(
        name='eam',
        version=__version__,
        author="Enthought Inc.",
        author_email="info@enthought.com",
        license='BSD-like',
        classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python'],
        install_requires=[
            'setuptools',
            'enum34; python_version < "3.4"',
            'comtypes; sys_platform == "win32"'],
        packages=find_packages(),
        zip_safe=False,
        entry_points={'console_scripts': 'eam = eam.cli:cli'},
        maintainer='Enthought Developers')
