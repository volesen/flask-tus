import sys
from setuptools import setup

setup(
    name="flask-tus",
    version="0.1",
    packages=["flask_tus", "flask_tus.models"],
    dependency_links=[],
    install_requires=[],
    extras_require={},
    package_data={},
    author="Vincent Olesen",
    author_email="private@email.com",
    description="Flask server for tus protocol",
    license="MIT",
    keywords=" documentation tutorial",
    url="http://github.com/volesen/flask-tus",
)
