from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="lch_scrapy",

    version="1.0.0",

    author="lichanghua",
    author_email="1371214116@qq.com",
    description="数据库etl包",
    long_description=open("README.txt", encoding="utf8").read(),

    url="https://github.com/",

    packages=find_packages(),

    # package_data={
    #     "lch_etl": [""]
    #
    # },

    install_requires=[
        "selenium","lch_etl",
    ],

    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5"
    ],
)
