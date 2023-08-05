# encoding: utf-8
# pylint: disable=missing-docstring

from __future__ import unicode_literals

from bugzilla_docstrings.parser import DocstringRecord, ValueRecord, get_docstrings_in_file

RESULTS = [
    DocstringRecord(
        lineno=3,
        column=4,
        value=[
            ValueRecord(lineno=1, column=8, value='12345656'),
            ValueRecord(lineno=2, column=8, value='* 1235623'),
            ValueRecord(lineno=3, column=8, value='12415')
        ],
        nodeid='tests/data/bz_doc_test.py::test_bugzilla1'
    ),
    DocstringRecord(
        lineno=17,
        column=4,
        value=[
            ValueRecord(lineno=1, column=8, value='12234'),
            ValueRecord(lineno=2, column=8, value='1243124, 124315, 1257643')],
        nodeid='tests/data/bz_doc_test.py::test_bugzilla2'
    )
]


def test_parser(source_file):
    docstrings = get_docstrings_in_file(source_file)
    assert len(docstrings) == len(RESULTS)
    assert docstrings == RESULTS
