#!/usr/bin/env python
from setuptools import setup, find_packages
from os import environ

setup(
  name="Workshops",
  version="0.0.1",
  package_dir={"": "src"},
  packages=find_packages("src"),
  include_package_data=True,
  install_requires=[
    "pygame"
  ],
)
