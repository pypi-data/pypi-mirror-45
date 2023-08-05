# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

with open("README.rst", "rb") as fp:
    LONG_DESCRIPTION = fp.read().decode("utf-8").strip()

setup(
    name="bugzilla-docstrings",
    version="0.0.1",
    url="https://gitlab.com/jdupuy/bugzilla_docstrings",
    description="Reads Bugzilla docstrings and validates them using flake8",
    long_description=LONG_DESCRIPTION,
    author="Martin Kourim",
    author_email="mkourim@redhat.com",
    license="MIT",
    packages=find_packages(exclude=("tests",)),
    setup_requires=["setuptools_scm"],
    install_requires=["pyyaml"],
    entry_points={
        "flake8.extension": ["B66 = bugzilla_docstrings.flake8_plugin:BugzillaDocstringsPlugin"]
    },
    keywords=["bugzilla", "testing"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
    ],
    include_package_data=True,
)
