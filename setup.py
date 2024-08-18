#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

from test_generator import __version__


def find_required():
    with open("requirements.txt") as f:
        return f.read().splitlines()


def find_dev_required():
    with open("requirements-dev.txt") as f:
        return f.read().splitlines()

setuptools.setup(
    name="test-generator",
    description="Script for generating tests",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    version=__version__,
    license="Apache-2.0",
    url="https://github.com/miner34006/test-generator",
    python_requires=">=3.7",
    packages=['test_generator'],
    install_requires=find_required(),
    tests_require=find_dev_required(),
    entry_points={
        'console_scripts': [
            'gena = test_generator.generate_scenarios:main',
        ]
    },
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
