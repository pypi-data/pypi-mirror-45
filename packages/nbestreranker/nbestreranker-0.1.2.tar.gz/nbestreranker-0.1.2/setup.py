#!/usr/bin/env python
# -*- coding:utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='nbestreranker',
    version="0.1.2",
    keywords=("pip", "nbest", "ranker"),
    description="nbest reranker nlp",
    long_description="nbest reranker",
    license="MIT Licence",
    url="https://github.com/GodsLeft",
    author="GodsLeft",
    author_email="1456466573@qq.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["numpy", "kenlm", "configreader", "argparse"],
    entry_points={
        'console_scripts': [
            'nbestreranker-augmenter = bin.augmenter',
            'nbestreranker-reranker = bin.reranker',
        ]
    }
)