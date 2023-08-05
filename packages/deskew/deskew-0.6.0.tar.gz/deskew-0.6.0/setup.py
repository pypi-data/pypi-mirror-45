#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='deskew',
    version='0.6.0',
    description='Skew detection and correction in images containing text',
    long_description="""Skew detection and correction in images containing text

Homepage: https://github.com/sbrunner/deskew""",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    author='Stéphane Brunner',
    author_email='stephane.brunner@gmail.com',
    url='https://github.com/sbrunner/deskew',
    packages=find_packages(exclude=['tests.*']),
    install_requires=['numpy', 'scikit-image!=0.15.0'],
    entry_points={
        'console_scripts': [
            'deskew = deskew.cli:main',
        ],
    },
)
