#!/usr/bin/env python3 

from setuptools import setup, find_packages
import os

setup(
  name='awsimagetag',
  version='1.6',
  author='Jasper Culong',
  author_email='jculongit10@yahoo.com',
  packages=find_packages(),
  license='LICENSE',
  description='AWS auto tagging tool',
  long_description=open('README.md').read(),
  url="https://pypi.org/project/aws-auto-tag-ami",
  entry_points={
    'console_scripts': [
        'awsimagetag = awsimagetag.core:main'
    ]
  },
  install_requires=[
    "boto3 >= 1.7.57",
    "twine == 1.13.0",
    "unittest2",
    "skew"
  ],
)