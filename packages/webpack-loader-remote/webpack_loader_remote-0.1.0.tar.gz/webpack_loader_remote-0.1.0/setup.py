#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import re
from setuptools import setup, find_packages

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_NAME = os.path.basename(PACKAGE_DIR)


def read_file(*parts):
    file_path = os.path.join(PACKAGE_DIR, *parts)
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def get_version():
    match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        read_file("src", PACKAGE_NAME, "__init__.py"),
        re.M
    )
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find version.")


setup(
    name=PACKAGE_NAME,
    version=get_version(),
    description="Load webpack stats from a local or remote file",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/alexseitsinger/{}".format(PACKAGE_NAME),
    author="Alex Seitsinger",
    author_email="contact@alexseitsinger.com",
    package_dir={"": "src"},
    packages=find_packages("src", exclude=["tests"]),
    install_requires=["requests"],
    include_package_data=True,
    license="MIT License",
    keywords=["django", "webpack"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
    ],
)
