#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import os
from setuptools import setup, find_packages


local_file = lambda *f: \
    open(os.path.join(os.path.dirname(__file__), *f), 'r').read()


class VersionFinder(ast.NodeVisitor):
    VARIABLE_NAME = 'version'

    def __init__(self):
        self.version = None

    def visit_Assign(self, node):
        try:
            if node.targets[0].id == self.VARIABLE_NAME:
                self.version = node.value.s
        except:
            pass


def read_version():
    finder = VersionFinder()
    finder.visit(ast.parse(local_file('grammarian', 'version.py')))
    return finder.version


setup(
    name='grammarian',
    version=read_version(),
    description="\n".join([
        'word definition lookup library',
    ]),
    entry_points={
    },
    author='Gabriel Falcao',
    author_email='gabriel@nacaolivre.org',
    url='https://github.com/gabrielfalcao/grammarian',
    packages=find_packages(exclude=['*tests*']),
    install_requires=[
        'beautifulsoup4',
        'pydictionary',
        'requests',
        'urbandictionary',
        'wikipedia',
    ],
    include_package_data=True,
    package_data={
        'grammarian': 'COPYING *.rst docs/*'.split(),
    },
    zip_safe=False,
)
