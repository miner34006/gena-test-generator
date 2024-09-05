import setuptools
from setuptools import find_packages

from test_generator.__version__ import __version__


def find_required():
    with open("requirements.txt") as f:
        return f.read().splitlines()


def find_dev_required():
    with open("requirements-dev.txt") as f:
        return f.read().splitlines()

setuptools.setup(
    name="gena-test-generator",
    description="Script for generating tests from Markdown files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    version=__version__,
    license="Apache-2.0",
    url="https://github.com/miner34006/gena-test-generator",
    python_requires=">=3.7",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    package_data={"test_generator": ["py.typed", "**/*.jinja"]},
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
