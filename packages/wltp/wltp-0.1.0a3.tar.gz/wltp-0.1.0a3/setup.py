#! python
#-*- coding: utf-8 -*-
#
# Copyright 2013-2014 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
''''Setuptools script for *wltp*, the WLTC gear-shift calculator.


Install:
========
Tested with Python 3.4.

To install it, assuming you have download the sources,
do the usual::

    python setup.py install

Or get it directly from the PIP repository::

    pip install wltp
'''
# Got ideas for project-setup from many places, among others:
#    http://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/
#    http://python-packaging-user-guide.readthedocs.org/en/latest/current.html

import os
import sys
import io
import re

from setuptools import setup, find_packages


# Fail early in ancient python-versions
#
py_ver = sys.version_info
if py_ver < (2, 7):
    exit("Sorry, Python2 >= 2.7 is supported!")
if py_ver >= (3,) and py_ver < (3, 3):
    exit("Sorry, Python3 >= 3.3 is supported!")
if sys.argv[-1] == 'setup.py':
    exit("To install, run `python setup.py install`")

proj_name = 'wltp'
mydir = os.path.dirname(__file__)


# Version-trick to have version-info in a single place,
# taken from: http://stackoverflow.com/questions/2058802/how-can-i-get-the-version-defined-in-setup-py-setuptools-in-my-package
##
def read_project_version():
    fglobals = {}
    with io.open(os.path.join(mydir, proj_name, '_version.py')) as fd:
        exec(fd.read(), fglobals)  # To read __version__
    return fglobals['__version__']


def read_text_lines(fname):
    with io.open(os.path.join(mydir, fname)) as fd:
        return fd.readlines()


def yield_rst_only_markup(lines):
    """
    :param file_inp:     a `filename` or ``sys.stdin``?
    :param file_out:     a `filename` or ``sys.stdout`?`

    """
    substs = [
        # Selected Sphinx-only Roles.
        #
        (r':abbr:`([^`]+)`', r'\1'),
        (r':ref:`([^`]+)`', r'ref: *\1*'),
        (r':term:`([^`]+)`', r'**\1**'),
        (r':dfn:`([^`]+)`', r'**\1**'),
        (r':(samp|guilabel|menuselection|doc|file):`([^`]+)`', r'``\2``'),

        # Sphinx-only roles:
        #        :foo:`bar`   --> foo(``bar``)
        #        :a:foo:`bar` XXX afoo(``bar``)
        #
        #(r'(:(\w+))?:(\w+):`([^`]*)`', r'\2\3(``\4``)'),
        #(r':(\w+):`([^`]*)`', r'\1(`\2`)'),
        # emphasis
        # literal
        # code
        # math
        # pep-reference
        # rfc-reference
        # strong
        # subscript, sub
        # superscript, sup
        # title-reference


        # Sphinx-only Directives.
        #
        (r'\.\. doctest', r'code-block'),
        (r'\.\. module', r'code-block'),
        (r'\.\. plot::', r'.. '),
        (r'\.\. seealso', r'info'),
        (r'\.\. glossary', r'rubric'),
        (r'\.\. figure::', r'.. '),
        (r'\.\. image::', r'.. '),

        (r'\.\. dispatcher', r'code-block'),

        # Other
        #
        (r'\|version\|', r'x.x.x'),
        (r'\|today\|', r'x.x.x'),
        (r'\.\. include:: AUTHORS', r'see: AUTHORS'),
    ]

    regex_subs = [(re.compile(regex, re.IGNORECASE), sub)
                  for (regex, sub) in substs]

    def clean_line(line):
        try:
            for (regex, sub) in regex_subs:
                line = regex.sub(sub, line)
        except Exception as ex:
            print("ERROR: %s, (line(%s)" % (regex, sub))
            raise ex

        return line

    for line in lines:
        yield clean_line(line)


proj_ver = read_project_version()


readme_lines = read_text_lines('README.rst')
description = readme_lines[1]
long_desc = ''.join(yield_rst_only_markup(readme_lines))
# Trick from: http://peterdowns.com/posts/first-time-with-pypi.html
download_url = 'https://github.com/ankostis/%s/tarball/v%s' % (
    proj_name, proj_ver)

setup(
    name=proj_name,
    version=proj_ver,
    description=description,
    long_description=long_desc,
    author="Kostis Anagnostopoulos @ European Commission (JRC)",
    author_email="ankostis@gmail.com",
    url="https://github.com/JRCSTU/wltp",
    download_url=download_url,
    license="European Union Public Licence 1.1 or later (EUPL 1.1+)",
    keywords=[
        "automotive", "vehicle", "vehicles", "car", "cars", "fuel", "gears", "gearshifs",
        "simulation", "simulator", "consumption", "driving", "engine", "wltc",
        "UNECE", "standard",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Development Status :: 3 - Alpha",
        'Natural Language :: English',
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(exclude=["wltp.test", "wltp.test.*"]),  # Wy need prune then??
    include_package_data=True,
    #     package_data= {'proj_name': ['data/*.csv']},
    #    package_data = {
    #        'wltp.excel': ['*.xlsm', '*.ico'],
    #    },
    install_requires=[
        'six',
        'jsonschema>=2.5',
        'numpy',
        'pandas',  # 'openpyxl', 'xlrd',
    ],
    setup_requires=[
        'setuptools-git >= 0.3',  # Gather package-data from all files in git.
    ],
    tests_require=[
        'nose',
        'coverage',
    ],
    extras_require={
        'plot': ['matplotlib'],  # need for docs to build & to run tests
        'excel': ['xlwings'],
        'wltpdb': [],
        ':python_version == "2.7"': ['mock'],
        ':platform_system=="Windows" or platform_system=="Darwin"':
        ['xlwings'],     # For Excel integration
    },
    test_suite='nose.collector',
    entry_points={
        'console_scripts': [
            'wltp = wltp.__main__:main',
        ],
    },
    zip_safe=True,
    options={
        'build_sphinx': {
            'build_dir': 'docs/_build',
        },
        'bdist_wheel': {
            'universal': True,
        },
    }
)
