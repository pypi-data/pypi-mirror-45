#
# Copyright (c) 2019, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from setuptools import setup

# Dynamically calculate the version based on proplan.VERSION.
version = __import__('proplan').get_version()

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='django-proplan',
    version=version,
    description=(
        'Django application to assign the tasks and planning of your project.'
    ),
    long_description=long_description,
    author='Grigoriy Kramarenko',
    author_email='root@rosix.ru',
    url='https://gitlab.com/djbaldey/django-proplan/',
    license='BSD License',
    platforms='any',
    zip_safe=False,
    packages=['proplan'],
    include_package_data=True,
    install_requires=[],
    classifiers=[
        # List of Classifiers: https://pypi.org/classifiers/
        'Development Status :: 1 - Planning',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
