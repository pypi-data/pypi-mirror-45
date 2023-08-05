#!/usr/bin/env python
# encoding: utf-8

"""Packaging script."""

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(here, 'README.rst')).read()

setup(
    name="licenseheaders",
    version="0.4",
    author="Johann Petrak",
    author_email="johann.petrak@gmail.com",
    description='Add or change license headers for all files in a directory',
    # TODO: change to markdown, text/markdown at some point
    long_description=readme,
    long_description_content_type="text/x-rst",
    setup_requires=[],
    install_requires=[],
    python_requires=">=3.5",
    license="MIT",
    keywords="",
    url="http://github.com/johann-petrak/licenseheaders",
    py_modules=['licenseheaders'],
    packages=find_packages(),
    package_data={'': ['templates/*']},
    include_package_data=True,
    entry_points={'console_scripts': ['licenseheaders=licenseheaders:main']},
    # test_suite='tests',
    # tests_require=['mock'],
    classifiers=["Development Status :: 5 - Production/Stable",
                 "License :: OSI Approved :: MIT License",
                 "Environment :: Console",
                 "Natural Language :: English",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3.3",
                 "Programming Language :: Python :: 3.4",
                 "Programming Language :: Python :: 3.5",
                 "Topic :: Software Development",
                 "Topic :: Software Development :: Code Generators",
                 "Intended Audience :: Developers",
                ],
)
