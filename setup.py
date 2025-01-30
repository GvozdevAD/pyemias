#!/usr/bin/env python
import os

from codecs import open
from setuptools import setup, find_packages


about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "src", "pyemias", "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), about)

with open("README.md", "r", "utf-8") as f:
    readme = f.read()

requires = [
    "beautifulsoup4==4.12.3",
    "certifi==2024.12.14",
    "charset-normalizer==3.4.1",
    "idna==3.10",
    "lxml==5.3.0",
    "nanoid==2.0.0",
    "requests==2.32.3",
    "soupsieve==2.6",
    "urllib3==2.3.0",
    "pydantic==2.10.6",
]

setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type='text/markdown',
    url=about["__url__"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"": ["LICENSE"]},
    include_package_data=True,
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords='emias pyemias',
    project_urls={},
    python_requires='>=3.10'
)