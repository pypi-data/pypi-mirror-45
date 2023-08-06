#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from __future__ import print_function


from os.path import dirname, join
from setuptools import setup, find_packages


def read_description():
    with open(join(dirname(__file__), 'README.md')) as file:
        return file.read()


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', ]

setup_requirements = ['pytest-runner', ]

extra_requirements = {
    'gpio': ['RPi.GPIO', ],
}

test_requirements = ['pytest', ]

setup(
    author="Christopher S. Fekete",
    author_email='cfekete93@hotmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description=(
        "Distributed control and communications system mainly "
        "targeted at single board computers such as the raspberry pi."
    ),
    entry_points={
        'console_scripts': [
            'pydracs=pydracs.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    keywords='pydracs',
    name='pydracs',
    packages=find_packages(),
    setup_requires=setup_requirements,
    extras_require=extra_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/cfekete93/pydracs',
    version='0.1.1',
    zip_safe=False,
)
