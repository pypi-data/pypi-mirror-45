#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(HERE, 'README.md')) as f:
    README = f.read()

setup(
    name='deskew',
    version='0.5.0',
    description='Skew detection and correction in images containing text',
    long_description=README,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    author='Stéphane Brunner',
    author_email='stephane.brunner@gmail.com',
    url='https://hub.docker.com/r/sbrunner/deskew/',
    packages=find_packages(exclude=['tests.*']),
    install_requires=['numpy', 'scikit-image'],
    entry_points={
        'console_scripts': [
            'deskew = deskew.cli:main',
        ],
    },
)
