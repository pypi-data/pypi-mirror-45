#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 09:10:09 2019

@author: Amine Laghaout
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='mlo',  
    version='0.0.2',
    scripts=[file+'.py' for file in ['main', 'problems', 'data_wranglers', 
                                     'estimators', 'visualizers', 
                                     'utilities']],
    author="Amine Laghaout",
    author_email="aknary@yahoo.com",
    description="Machine learning objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/laghaout/machine-learning-toolbox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
)