import os

from setuptools import setup

setup(
    name='aldebaran',
    version='0.1.2',
    description='Aldebaran Python Client',
    long_description='Aldebaran Python Client is a client library for accessing Aldebaran from python code. This library also gets bundled with any Python algorithms in Aldebaran.',
    url='https://aldebaran.signate.jp',
    author='SIGNATE Inc.',
    packages=['Aldebaran'],
    install_requires=[
        'requests',
        'six',
        'enum34'
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
