#! /usr/bin/env python
from setuptools import setup, find_packages

import versioneer


setup(
    name="py-scripting",
    version=versioneer.get_version(),
    description="Python utilities for scripting",
    long_description=open("README.rst").read(),
    author="Eric Hutton",
    author_email="huttone@colorado.edu",
    url="http://csdms.colorado.edu",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    install_requires=["six"],
    setup_requires=["setuptools"],
    packages=find_packages(),
    cmdclass=versioneer.get_cmdclass(),
)
