
import os
import sys

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()
from setuptools import setup

setup(
    name="syspath_fixer",
    version="1.0.0",
    url="https://github.com/TeodorIvanov/feedfinder3",
    license="MIT",
    author="Teodor Ivanov",
    author_email="tdrivanov@gmail.com",
    description="add modules to syspath easily",
    long_description="add modules to syspath easily",
    py_modules=["syspath_fixer"],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Natural Language :: English",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
