#!/usr/bin/env python
import setuptools

with open('README.md') as readme:
    long_description = readme.read()

with open('requirements.txt') as requirements:
    install_requires = [x.strip() for x in requirements.read().split(
        '\n') if not x.startswith('#')]

setuptools.setup(
    name="flask-tus",
    version="0.1",
    author="Vincent Olesen",
    author_email="private@email.com",
    description="Tus protocol 1.0.0 server implementation for Flask",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/volesen/flask-tus",
    packages=setuptools.find_packages(),
    install_requires=install_requires, 
    tests_require=['pytest>=4.0.0'],
    zip_safe=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'flask.commands': [
            'tus=flask_tus.manage.commands:cli'
        ],
    }
)
