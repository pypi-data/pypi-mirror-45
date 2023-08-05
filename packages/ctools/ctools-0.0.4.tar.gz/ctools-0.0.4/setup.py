# -*- coding: utf-8 -*-
import io
from setuptools import setup, Extension

extra_compile_args = ["-std=c99", "-Wall", "-Wextra"]

extensions = [
    Extension("ctools", ["ctoolsmodule.c"], extra_compile_args=extra_compile_args),
]

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name="ctools",
    version="0.0.4",
    author="hanke",
    author_email="hanke0@outlook.com",
    description="A collection of useful extensions for python implement in C.",
    url="https://github.com/ko-han/python-ctools",
    license='MIT',
    long_description=readme,
    long_description_content_type='text/x-rst',
    python_requires=">=3",
    include_package_data=True,
    zip_safe=False,
    ext_modules=extensions,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
