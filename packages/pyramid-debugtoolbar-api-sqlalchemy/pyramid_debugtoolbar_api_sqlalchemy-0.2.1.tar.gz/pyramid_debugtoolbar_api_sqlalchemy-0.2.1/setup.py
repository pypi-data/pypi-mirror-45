"""pyramid_debugtoolbar_api_sqlalchemy installation script.
"""
import os
from setuptools import setup
from setuptools import find_packages

# store version in the init.py
import re
with open(
        os.path.join(
            os.path.dirname(__file__),
            'pyramid_debugtoolbar_api_sqlalchemy', '__init__.py')) as v_file:
    VERSION = re.compile(
        r".*__VERSION__ = '(.*?)'",
        re.S).match(v_file.read()).group(1)

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md")).read()
README = README.split("\n\n", 1)[0] + "\n"

requires = ['pyramid_debugtoolbar>=4.0',
            'six',
            ]

setup(
    name="pyramid_debugtoolbar_api_sqlalchemy",
    author="Jonathan Vanasco",
    author_email="jonathan@findmeon.com",
    url="https://github.com/jvanasco/pyramid_debugtoolbar_api_sqlalchemy",
    version=VERSION,
    description="SqlAlchemy exporting for pyramid_debugtoolbar",
    keywords="web pyramid",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Framework :: Pyramid",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    long_description=README,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    test_suite="tests",
)
