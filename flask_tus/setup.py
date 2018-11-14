import sys
from setuptools import setup

setup(
    name = "flask-tus",        # what you want to call the archive/egg
    version = "0.1",
    packages=["flask_tus"],    # top-level python modules you can import like
                                #   'import foo'
    dependency_links = [],      # custom links to a specific project
    install_requires=[],
    extras_require={},      # optional features that other packages can require
                            #   like 'helloworld[foo]'
    package_data = {},
    author="Vincent Olesen",
    author_email = "private@email.com",
    description = "Flask server for tus protocol",
    license = "MIT",
    keywords= " documentation tutorial",
    url = "http://github.com/volesen/flask-tus",
)
