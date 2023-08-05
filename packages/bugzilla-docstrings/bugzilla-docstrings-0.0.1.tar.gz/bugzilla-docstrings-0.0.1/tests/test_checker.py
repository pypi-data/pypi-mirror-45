# encoding: utf-8
# pylint: disable=missing-docstring

from __future__ import unicode_literals

from bugzilla_docstrings import checker


RESULTS = [
    (5, 8, 'B664 Invalid value "* 1235623" of the Bug ID'),
    (19, 8, 'B664 Invalid value "1243124, 124315, 1257643" of the Bug ID')
]


def _strip_func(errors):
    return [(lineno, col, msg) for lineno, col, msg, __ in errors]


def test_checker(source_file):
    errors = checker.DocstringsChecker(None, source_file, {}, "TestChecker").run_checks()
    errors = _strip_func(errors)
    assert len(errors) == len(RESULTS)
    assert errors == RESULTS
