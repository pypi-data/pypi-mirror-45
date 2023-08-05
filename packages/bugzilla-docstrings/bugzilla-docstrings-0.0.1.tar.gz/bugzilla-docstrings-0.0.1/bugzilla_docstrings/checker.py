# -*- coding: utf-8 -*-
# pylint: disable=useless-object-inheritance
"""
Checks Polarion docstrings.
"""

from __future__ import absolute_import, print_function, unicode_literals

import os
import re
import sys
from collections import namedtuple

from bugzilla_docstrings import parser

DocstringsError = namedtuple("DocstringsError", "lineno column message checker")
FieldRecord = namedtuple("FieldRecord", "lineno column value")
ValidatedDocstring = namedtuple("ValidatedDocstring", "invalid")


# pylint: disable=too-many-instance-attributes
class DocstringsChecker(object):
    """Checker for Bugzilla docstrings."""

    INVALID_VALUE = "B664"

    def __init__(self, tree, filename, config, checker):
        self.tree = tree
        self.filename = filename
        self.config = self.get_valid_config(config)
        self.checker = checker or "DocstringsChecker"
        self.set_compiled_lists()

    def set_compiled_lists(self):
        """Sets compiled regular expressions for whitelist and blacklist.

        Uses values set in config if available so the compilation doesn't need to
        be repeated with every instantiation.
        """
        if "_compiled_blacklist" in self.config:
            self._compiled_whitelist = self.config.get("_compiled_whitelist")
            self._compiled_blacklist = self.config.get("_compiled_blacklist")
        else:
            self._compiled_whitelist, self._compiled_blacklist = self.get_compiled_lists(
                self.config
            )

    @staticmethod
    def get_valid_config(config):
        """Returns valid configuration if available."""
        cfg_valid = config.get("docstrings") or {}
        cfg_valid = cfg_valid.get("valid_values")
        if not (cfg_valid and config.get("default_fields")):
            return {}
        return config

    @staticmethod
    def get_compiled_lists(config):
        """Returns compiled regular expressions for whitelist and blacklist."""
        compiled_whitelist, compiled_blacklist = None, None
        if config.get("whitelisted_tests"):
            compiled_whitelist = re.compile("(" + ")|(".join(config.get("whitelisted_tests")) + ")")
        if config.get("blacklisted_tests"):
            compiled_blacklist = re.compile("(" + ")|(".join(config.get("blacklisted_tests")) + ")")
        return compiled_whitelist, compiled_blacklist

    @staticmethod
    def validate_value(docstring_dict, key, valid_values):
        record = docstring_dict.get(key)
        if record is not None:
            return record.value in valid_values[key]
        return True

    @classmethod
    def get_invalid_fields(cls, docstring_value):
        """ Check that bug ids are numbers """
        invalid = []
        for value_record in docstring_value:
            # check if string is a digit
            okay = value_record.value.isdigit()
            if not okay:
                invalid.append(
                    FieldRecord(
                        value_record.lineno, value_record.column, value_record.value
                    )
                )

        return invalid

    def validate_docstring(self, docstring_value):
        """Returns tuple with lists of problematic fields."""
        invalid = self.get_invalid_fields(docstring_value)
        return ValidatedDocstring(invalid)

    # pylint:disable=too-many-locals
    def get_fields_errors(self, validated_docstring, lineno=0):
        """Produces fields errors for the flake8 checker."""
        errors = []

        for num, col, value in validated_docstring.invalid:
            errors.append(
                DocstringsError(
                    lineno + num,
                    col,
                    '{} Invalid value "{}" of the Bug ID'.format(
                        self.INVALID_VALUE, value,
                    ),
                    self.checker,
                )
            )

        if errors:
            errors = sorted(errors, key=lambda tup: tup[0])
        return errors

    @staticmethod
    def print_errors(errors):
        """Prints errors without using flake8."""
        for err in errors:
            print("line: {}:{}: {}".format(err.lineno, err.column, err.message), file=sys.stderr)

    def check_docstrings(self, docstrings_in_file):
        """Runs checks on each docstring."""
        errors = []
        for docstring in docstrings_in_file:
            if not self.is_nodeid_whitelisted(docstring.nodeid):
                continue
            if docstring.value:
                valdoc = self.validate_docstring(docstring.value)
                errors.extend(
                    self.get_fields_errors(
                        valdoc, docstring.lineno
                    )
                )
            else:
                # bugzilla section is not required, so pass if it isn't present
                pass

        return errors

    def run_checks(self):
        """Checks docstrings in python source file."""
        docstrings_in_file = parser.get_docstrings_in_file(self.filename, tree=self.tree)
        errors = self.check_docstrings(docstrings_in_file)
        return errors

    def is_nodeid_whitelisted(self, nodeid):
        """Checks if the nodeid is whitelisted."""
        if not nodeid:
            return True
        if self._compiled_whitelist and self._compiled_whitelist.search(nodeid):
            return True
        if self._compiled_blacklist and self._compiled_blacklist.search(nodeid):
            return False
        return True

    def is_file_for_check(self):
        """Decides if the file should be checked."""
        # if not self.config:
        #     return False

        abs_filename = os.path.abspath(self.filename)
        head, tail = os.path.split(abs_filename)

        # check only test files under polarion tests path
        if not tail.startswith("test_"):  # and utils.find_tests_marker(head or ".")):
            return False

        return True

    def get_errors(self):
        """Get errors in docstrings in python source file."""
        if not self.is_file_for_check():
            return []

        return self.run_checks()
