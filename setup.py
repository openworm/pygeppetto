#!/usr/bin/env python

from setuptools import setup, find_packages

__version__ = "0.1.0"

setup(
    name="pygeppetto",
    version=__version__,
    description=("Geeppetto Python API."
                 "The API allows to create a Geppetto Model from Python."),
    long_description=open('README.md').read(),
    keywords="geppetto openworm Python",
    url="https://github.com/openworm/pygeppetto",
    packages=find_packages(),
    package_data={'': ['README.md']},
    include_package_data=True,
    install_requires=['pyecore>=0.2.0'],
    extras_require={'testing': ['pytest']},
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries"
    ]
)
