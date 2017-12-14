#!/usr/bin/env python3
# coding: utf8

from setuptools import setup, find_packages
from codecs import open
from os import path


NAME = 'vk7'
VERSION = __import__(NAME).__version__
DESCRIPTION = 'Framework for extract data from vk.com (russian social network).'
URL = 'https://github.com/pash4paul/vk7'
AUTHOR = 'Pavel Fomin'
AUTHOR_EMAIL = 'pash4paul@gmail.com'


cwd = path.abspath(path.dirname(__file__))
with open(path.join(cwd, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='api data osint social vk.com',
    packages=find_packages(exclude=['tests']),
    install_requires='requests==2.18.4'
)
