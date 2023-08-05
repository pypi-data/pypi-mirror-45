import io
import json
import os
import re
import importlib

from setuptools import find_packages, setup

CONFIG_FILE = "etler/config.py"


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding="utf-8") as fd:
        return re.sub(text_type(r":[a-z]+:`~?(.*?)`"), text_type(r"``\1``"), fd.read())


version = importlib.import_module(CONFIG_FILE).fetch("version")

install_requires = []
tests_require = []

with open("Pipfile.lock") as fd:
    lock_data = json.load(fd)
    install_requires = [
        package_name + package_data["version"]
        for package_name, package_data in lock_data["default"].items()
    ]
    tests_require = [
        package_name + package_data["version"]
        for package_name, package_data in lock_data["develop"].items()
    ]


setup(
    name="etler",
    version=version,
    url="https://github.com/sdll/etler",
    license="MIT",
    author="Sasha Illarionov",
    author_email="sasha@sdll.space",
    description="Python ETL Utilities",
    long_description=read("README.rst"),
    packages=find_packages(exclude=("tests",)),
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
