from __future__ import print_function
#!/usr/bin/env python
# coding=utf-8


from setuptools import setup, find_packages

import luoluo
setup(
    name='luoluo',
    version='1.0',
    description=(
        'A toolkits for myself'
    ),
    long_description= '',
    author='Andy Wong',
    author_email='pku_weijia@163.com',
    maintainer='Andy Wong',
    maintainer_email='pku_weijia@163.com',
    license='BSD License',
    packages=['luoluo'],
    platforms=["all"],
    url='http://www.weijiaw.cn',
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