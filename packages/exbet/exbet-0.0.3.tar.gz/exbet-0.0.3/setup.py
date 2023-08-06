#!/usr/bin/env python3

from setuptools import setup

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs

try:
    codecs.lookup("mbcs")
except LookupError:
    ascii = codecs.lookup("ascii")
    codecs.register(lambda name, enc=ascii: {True: enc}.get(name == "mbcs"))

VERSION = "0.0.3"

setup(
    name="exbet",
    version=VERSION,
    description="Python library for Exbet",
    long_description=open("README.md").read(),
    download_url="",
    author="exbet.io",
    author_email="py@exbet.io",
    maintainer="exbet.io",
    maintainer_email="py@exbet.io",
    url="http://exbet.io",
    keywords=["exbet", "library", "api", "rpc"],
    packages=[],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Games/Entertainment",
    ],
    entry_points={"console_scripts": ["exbet = exbet.cli.cli:main"]},
    install_requires=open("requirements.txt").readlines(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    include_package_data=True,
)
