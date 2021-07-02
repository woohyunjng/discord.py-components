import re
from codecs import open
from os import environ

from setuptools import find_packages, setup
from discord_components import __version__ as tempversion

PACKAGE_NAME = "discord_components"

with open("README.md", "r", encoding="utf-8") as f:
    README = f.read()

try:
    version = (
        environ["TRAVIS_TAG"].lstrip("v")
        if environ["TRAVIS"] == "true"
        else environ["VERSION_NUMBER"]
    )
except KeyError:
    version = tempversion

setup(
    name=PACKAGE_NAME,
    version=version,
    author="kiki7000",
    author_email="devkiki7000@gmail.com",
    description="An unofficial library for discord components.",
    include_package_data=True,
    install_requires=["discord.py", "aiohttp"],
    license="MIT License",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/discord.py-components/discord.py-components",
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)
