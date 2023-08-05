#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
import os
from setuptools import setup, find_packages

root = os.path.dirname(__file__)


with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'six'
]
setup_requirements = [
    'pytest-runner',
    'wheel',
    'twine',
    'pytest',
    'pytest-runner',
    'pylint',
    'tox',
]
test_requirements = ['pytest', ]

setup(
    author="Alex Hatfield",
    author_email='alex@hatfieldfx.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python program communication interface",
    entry_points={
        'console_scripts': [
            'net=net.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='app-net',
    name='app-net',
    packages=find_packages(include=['net', 'net.connections', 'net.defaults', 'net.peer']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/aldmbmtl/net',
    version='0.6.1',
    zip_safe=False,
)
