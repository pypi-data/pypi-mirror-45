# -*- coding: utf-8 -*-
try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools.")

import os
if os.path.exists("README.txt"):
    long_description = open('README.txt').read()

setup(
    name='make_corpus',
    version='0.0.2',
    description='maiking corpus from a sentence',
    author='Takaaki Miwa',
    author_email='cryptofran1@gmail.com',
    install_requires=['numpy'],
    url='https://github.com/kennethreitz/samplemod',
    license="MIT",
    packages=find_packages(exclude=('tests', 'docs')),
)
