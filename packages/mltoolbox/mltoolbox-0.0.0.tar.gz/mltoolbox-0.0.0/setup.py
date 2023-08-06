#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Thu Apr 25 09:10:09 2019

@author: Amine Laghaout
'''

import pathlib
from setuptools import find_packages, setup

NAME = 'mltoolbox'                          # Package name
HERE = pathlib.Path(__file__).parent        # Currenty directory
README = (HERE / 'README.md').read_text()   # Long description

setup(
    name=NAME,
    version='0.0.0',
    description='Machine learning toolbox',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/laghaout/machine-learning-toolbox',
    author='Amine Laghaout',
    author_email='aknary@yahoo.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    install_requires=['keras', 'matplotlib', 'pandas', 'sklearn'],
)