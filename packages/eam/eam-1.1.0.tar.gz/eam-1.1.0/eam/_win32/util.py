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
from ctypes import WinError, POINTER, c_wchar_p
from ctypes.wintypes import DWORD, LPARAM

DWORD_PTR = POINTER(DWORD)
PDWORD_PTR = POINTER(DWORD_PTR)
LPTSTR = c_wchar_p
LRESULT = LPARAM


def function_factory(
        function, argument_types=None,
        return_type=None, error_checking=None):
    if argument_types is not None:
        function.argtypes = argument_types
    function.restype = return_type
    if error_checking is not None:
        function.errcheck = error_checking
    return function


def make_error(function, function_name=None):
    if function_name is None:
        function_name = function.__name__
    exception = WinError()
    exception.function = function_name
    return exception


def check_null_factory(function_name=None):
    def check_null(result, function, arguments, *args):
        if result is None:
            raise make_error(function, function_name)
        return result
    return check_null


check_null = check_null_factory()


def check_zero_factory(function_name=None):
    def check_zero(result, function, arguments, *args):
        if result == 0:
            raise make_error(function, function_name)
        return result
    return check_zero


check_zero = check_zero_factory()


def check_hresult_factory(function_name=None):
    def check_hresult(result, function, arguments, *args):
        if result != 0:
            raise make_error(function, function_name)
        return result
    return check_hresult


check_hresult = check_hresult_factory()
