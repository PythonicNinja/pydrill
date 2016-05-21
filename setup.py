#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = open('requirements_base.txt', 'r').readlines()

test_requirements = open('requirements_testing.txt', 'r').readlines()

setup(
    name='pydrill',
    version='0.1.1',
    description="Python Driver for Apache Drill.",
    long_description=readme + '\n\n' + history,
    author="Wojciech Nowak",
    author_email='mail@pythonic.ninja',
    url='https://github.com/PythonicNinja/pydrill',
    packages=find_packages(
        where='.',
        exclude=('test_*', )
    ),
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='pydrill',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
