#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://dot_configs.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='dot_configs',
    version='0.1.1',
    description='Import and handle project configurations as dot-separated configs object',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Magnus "Loxosceles" Henkel',
    author_email='loxosceles@gmx.de',
    url='https://gitlab.com/loxosceles/dot_configs',
    packages=[
        'dot_configs',
    ],
    package_dir={'dot_configs': 'dot_configs'},
    include_package_data=True,
    install_requires=[
    ],
    license='GNU GPL v3.0',
    zip_safe=False,
    keywords='dot_configs',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
