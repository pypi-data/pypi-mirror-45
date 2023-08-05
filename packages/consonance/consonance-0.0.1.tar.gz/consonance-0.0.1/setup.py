# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name='consonance',
    version="0.0.1",
    packages=find_packages(exclude=['tests', 'examples']),
    license='MIT',
    author='Tarek Galal',
    author_email='tare2.galal@gmail.com',
    description="",
    long_description="",
    platforms='any',
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.5',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Operating System :: MacOS :: MacOS X',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX :: Linux',
                 'Topic :: Security :: Cryptography',
                 'Topic :: Software Development :: Libraries :: Python Modules']
)
