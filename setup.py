# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

NAME = 'rome'
VERSION = '0.1'

requires = ['Babel',
            'nose']

setup(name=NAME,
      version=VERSION,
      packages=find_packages(),
      install_requires=requires,
      tests_require=requires,
      test_suite="nose.collector",
      message_extractors = { '.': [
        ('**.py', 'python', None),]})
