#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='django-contento',
    version='0.1b',
    description='Very basic CMS',
    author='Kamil Selwa',
    author_email='selwak@gmail.com',
    url='http://github.com/k1000/django-contento/tree/master',
    packages = find_packages(exclude=['examples', 'tests']),
    # include_package_data=True,
    zip_safe=False,
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Web Environment',
                 'Framework :: Django',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Utilities'],
    install_requires=['django-yamlfield', ],
    license='BSD',
    test_suite = "contento.tests",
)
