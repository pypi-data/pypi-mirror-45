# Copyright (c) 2015 - Red Hat Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.  See http://www.gnu.org/copyleft/gpl.html for
# the full text of the license.


"""Miscellaneous utilities

This module contains a bunch of utilities used elsewhere in pyrpkg.
"""


import argparse
import os
import sys

import six

if six.PY3:
    def u(s):
        return s

    getcwd = os.getcwd
else:
    def u(s):
        return s.decode('utf-8')

    getcwd = os.getcwdu


class cached_property(property):
    """A property caching its return value

    This is pretty much the same as a normal Python property, except that the
    decorated function is called only once. Its return value is then saved,
    subsequent calls will return it without executing the function any more.

    Example:
        >>> class Foo(object):
        ...     @cached_property
        ...     def bar(self):
        ...         print("Executing Foo.bar...")
        ...         return 42
        ...
        >>> f = Foo()
        >>> f.bar
        Executing Foo.bar...
        42
        >>> f.bar
        42
    """
    def __get__(self, inst, type=None):
        try:
            return getattr(inst, '_%s' % self.fget.__name__)
        except AttributeError:
            v = super(cached_property, self).__get__(inst, type)
            setattr(inst, '_%s' % self.fget.__name__, v)
            return v


def warn_deprecated(clsname, oldname, newname):
    """Emit a deprecation warning

    :param str clsname: The name of the class which has its attribute
        deprecated.
    :param str oldname: The name of the deprecated attribute.
    :param str newname: The name of the new attribute, which should be used
        instead.
    """
    sys.stderr.write(
        "DeprecationWarning: %s.%s is deprecated and will be removed eventually.\n"
        "Please use %s.%s instead.\n" % (clsname, oldname, clsname, newname))


def _log_value(log_func, value, level, indent, suffix=''):
    offset = ' ' * level * indent
    log_func(''.join([offset, str(value), suffix]))


def log_result(log_func, result, level=0, indent=2):
    if isinstance(result, list):
        for item in result:
            log_result(log_func, item, level)
    elif isinstance(result, dict):
        for key, value in result.items():
            _log_value(log_func, key, level, indent, ':')
            log_result(log_func, value, level+1)
    else:
        _log_value(log_func, result, level, indent)


def find_me():
    """Find the way to call the same binary/config as is being called now"""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '-C', '--config', help='Specify a config file to use')
    (args, other) = parser.parse_known_args()

    binary = os.path.abspath(sys.argv[0])

    cmd = [binary]
    if args.config:
        cmd += ['--config', args.config]

    return cmd


def validate_module_dep_override(dep):
    """Validate the passed-in module dependency override."""
    try:
        return dep.split(':', 1)
    except (ValueError, AttributeError):
        raise argparse.ArgumentTypeError('This option must be in the format of "name:stream"')


def validate_module_build_optional(optional_arg):
    """Validate the passed-in optional argument to the module-build command."""
    try:
        key, value = optional_arg.split('=', 1)
    except (ValueError, AttributeError):
        raise argparse.ArgumentTypeError('This option must be in the format of "key=value"')

    if key in ('branch', 'buildrequire_overrides', 'require_overrides', 'scmurl'):
        raise argparse.ArgumentTypeError(
            'The "{0}" optional argument is reserved to built-in arguments'.format(key))

    return (key, value)
