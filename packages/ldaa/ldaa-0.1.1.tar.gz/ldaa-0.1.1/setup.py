#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 17:17:09 2019

@author: ricky
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ldaa",
    version="0.1.1",                        # Update this for every new version
    author="Zhen Han Si & Zixi Wang",
    author_email="zs85@duke.edu",
    description="long description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[                      # Add project dependencies here
        "pandas>=0.20.0"                    # example: pandas version 0.20 or greater                          
    ],                                             
    url="https://github.com/BillyWangwzx/LDA-with-python",  
    packages=setuptools.find_packages(),
    classifiers=(                                 # Classifiers help people find your 
        "Programming Language :: Python :: 3",    # projects. See all possible classifiers 
        "License :: OSI Approved :: MIT License", # in https://pypi.org/classifiers/
        "Operating System :: OS Independent",   
    ),
)
