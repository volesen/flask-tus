#!/usr/bin/env python
from setuptools import setup

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name="flask-tus",
    version="0.1",
    packages=["flask_tus", "flask_tus.models"],
    dependency_links=[],
    install_requires=['Flask == 1.0.2'],
    test_requires=['pytest'],
    extras_require={},
    package_data={},
    author="Vincent Olesen",
    author_email="private@email.com",
    description="Tus protocol 1.0.0 Flask server implementation",
    long_description=long_description,
    license="MIT",
    keywords=" documentation tutorial",
    url="http://github.com/volesen/flask-tus",
)
