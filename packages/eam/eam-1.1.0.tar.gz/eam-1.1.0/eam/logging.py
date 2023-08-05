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
from __future__ import absolute_import

import logging
import logging.config
import logging.handlers
import os.path
import warnings

from .fileutils import makedirs
from . import __version__

logger = logging.getLogger(__name__)


class RotatingFileHandler(logging.handlers.RotatingFileHandler):
    def _open(self):
        makedirs(os.path.dirname(self.baseFilename))
        return logging.handlers.RotatingFileHandler._open(self)


def enable_logging(verbosity_level, log_filename=None):
    if verbosity_level is None and log_filename is None:
        return
    elif verbosity_level is None:
        level = logging.WARN
    elif verbosity_level >= 2:
        level = logging.DEBUG
    elif verbosity_level == 1:
        level = logging.INFO
    else:
        level = logging.WARN

    root_level = level
    if log_filename is not None:
        log_path = os.path.abspath(log_filename)
        disable = False
        try:
            makedirs(os.path.dirname(log_path))
        except OSError:
            disable = True
        else:
            try:
                with open(log_path, "a"):
                    pass
            except OSError:
                disable = True
        if disable:
            warnings.warn(
                "No write access to '{}', disabling file logging".
                format(log_filename))
            log_filename = None
    if log_filename is not None:
        root_level = logging.DEBUG

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "f": {"format": "%(asctime)s [%(name)s:%(lineno)s] %(message)s"}},
        "handlers": {
            "console": {
                "level": level,
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout"},
            "user_log": {
                "level": "DEBUG",
                "class": "eam.logging.RotatingFileHandler",
                "filename": log_filename or "/dev/null",
                "maxBytes": 1014 ** 2 * 8,
                "delay": True,
                "formatter": "f"}},
        "root": {
            "level": root_level,
            "handlers": [
                entry
                for entry in ("console", "user_log" if log_filename else None)
                if entry is not None]}})

    msg = "Using eam version {}".format(__version__)
    logger.info(msg)
