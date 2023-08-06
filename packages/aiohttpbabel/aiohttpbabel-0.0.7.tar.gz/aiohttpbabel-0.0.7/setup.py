# -*- coding: utf-8 -*-
"""
    Babel localisation support for aiohttp
"""
from setuptools import setup
from setuptools import find_packages

setup(
    name = "aiohttpbabel",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    packages=find_packages(),

    install_requires = [
        "aiohttp",
        "babel",
        "speaklater",
    ],

    author = "zhouyang",
    author_email = "zhouyang@zhouyang.me",
    description = "Babel localisation support for aiohttp",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    license = "BSD",
    keywords = "aiohttp locale babel localisation",
    url = "https://gitlab.com/nicofonk/aiohttp-babel",
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ]
)
