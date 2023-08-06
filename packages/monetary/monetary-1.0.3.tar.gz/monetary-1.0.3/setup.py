# -*- coding: utf-8 -*-

from setuptools import setup


version = '1.0.3'


setup(
    name='monetary',
    version=version,
    keywords='Currency Monetary Convert',
    description='Currency Convert',
    long_description=open('README.rst').read(),

    url='https://github.com/CurrencyClub/monetary',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['monetary'],
    py_modules=[],
    install_requires=[],

    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
