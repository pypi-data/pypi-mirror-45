# coding=utf-8
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='request_log_info',
    version='0.0.1',
    description='',
    long_description=long_description,
    author='zhangruyu',
    author_email='1582034460@qq.com',
    license="BSD",
    url='https://github.com/zhangruyu/request_log_info',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
