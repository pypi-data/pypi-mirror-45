#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='one-line-catch',
    version='1.0.0',
    description=(
        'try except and set-trace in one line with content manager'
    ),
    long_description='using context manager to achieve one line set_trace,\
    since there is no local variable recorded, inspect module is used to \
    recover nonlocal variable in dict variable: nonlocals',
    author='Primus Zhao',
    author_email='python4699680@gmail.com',
    maintainer='Primus Zhao',
    maintainer_email='python4699680@gmail.com',
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    url='',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires = ['ipdb']
)
