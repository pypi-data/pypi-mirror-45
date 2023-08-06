#!/usr/bin/env python
import setuptools

with open('README.md', 'r', encoding='utf-8') as fp:
    long_desc = fp.read()

setuptools.setup(
    name='bg-qsp',
    version='0.1.3',
    packages=['bgqsp',],
    license='MIT LICENSE',
    author='Bart Mosley',
    author_email='bartm@bondgeek.com',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://github.com/bondgeek/bgqsp',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
