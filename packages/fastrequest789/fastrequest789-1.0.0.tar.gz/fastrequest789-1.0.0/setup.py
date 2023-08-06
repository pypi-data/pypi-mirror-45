# !/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "fastrequest789",
    version = "1.0.0",
    keywords = ("pip", "requests","aiohttp", "spider"),
    description = "fast requests",
    long_description = "Aiohttp is encapsulated to keep the speed of asynchronism, and it can be used as simple and convenient as requests.",
    license = "MIT Licence",
    url = "https://github.com/ayong1/-",
    author = "ayong01",
    author_email = "13026391531@163.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['aiohttp','lxml']
)
