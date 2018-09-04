#!/usr/bin/env python

from setuptools import setup, find_packages
import sys

__version__ = "0.4.1"

if sys.version_info < (3, 3):
    required_packages = ['pyecore-py2']
else:
    required_packages = ['pyecore']


setup(
    name="pygeppetto",
    version=__version__,
    description=("Geppetto Python API for creating a Geppetto Model from Python"),
    author="The Geppetto Development Team",
    author_email="info@geppetto.org",
    license="MIT",
    long_description=open('README.rst').read(),
    keywords="geppetto openworm Python",
    url="https://github.com/openworm/pygeppetto",
    packages=find_packages(),
    package_data={'': ['README.md']},
    include_package_data=True,
    install_requires=required_packages,
    extras_require={'testing': ['pytest']},
    classifiers=[
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries"
    ]
)
