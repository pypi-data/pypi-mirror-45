#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='seisample',
    version='1.0.1',
    description=(
        'to generate seismic samples'
    ),
    long_description=open('README.rst').read(),
    author='siwei',
    author_email='siweiyu.hit@foxmail.com',
    maintainer='siweiyu',
    maintainer_email='siweiyu.hit@foxmail.com',
    license='BSD License',
    packages=['python_segy'],
    platforms=["all"],
    url='http://homepage.hit.edu.cn/pages/siweiyu',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
