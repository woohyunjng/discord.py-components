from os import environ
from setuptools import setup, find_packages

from discord_components import (
    __author__ as author,
    __license__ as _license,
    __name__ as name,
)

version = (
    environ["TRAVIS_TAG"].lstrip("v") if environ["TRAVIS"] == "true" else environ["VERSION_NUMBER"]
)

setup(
    name=name,
    version=version,
    license=_license,
    author=author,
    author_email="devkiki7000@gmail.com",
    description="unofficial library for discord components(on development)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kiki7000/discord.py-components",
    packages=find_packages(),
    install_requires=open("requirements.txt").readlines(),
    python_requires=">=3.8",
)
