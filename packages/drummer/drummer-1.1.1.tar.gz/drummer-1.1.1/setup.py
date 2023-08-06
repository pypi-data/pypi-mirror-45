#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os import path as os_path

# short/long description
short_desc = 'A multi-process, multi-tasking job scheduler'
here = os_path.abspath(os_path.dirname(__file__))
try:
    with open(os_path.join(here,'README.md'),'r',encoding='utf-8') as f:
        long_desc = '\n' + f.read()
except FileNotFoundError:
    long_desc = short_desc

setup(
    name='drummer',
    version='1.1.1',
    description=short_desc,
    author='andrea capitanelli',
    author_email='andrea.capitanelli@gmail.com',
    maintainer='andrea capitanelli',
    maintainer_email='andrea.capitanelli@gmail.com',
    url='https://github.com/acapitanelli/drummer',
    packages=find_packages(),
    install_requires=[
        'blessings',
        'croniter',
        'inquirer',
        'PTable',
        'PyYAML',
        'readchar',
        'six',
        'SQLAlchemy',
    ],
    long_description=long_desc,
    long_description_content_type='text/markdown',
    keywords='scheduler extender multi-process multi-tasking',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: System'
    ],
    scripts=[
        os_path.join(here,'bin/drummer-admin')
    ]
)
