from os import environ
from setuptools import setup, find_packages

from discord_components import (
    __author__ as author,
    __version__ as tempversion,
    __license__ as _license,
    __name__ as name,
)

try:
    version = (
        environ["TRAVIS_TAG"].lstrip("v")
        if environ["TRAVIS"] == "true"
        else environ["VERSION_NUMBER"]
    )
except KeyError:
    version = tempversion

setup(
    name="discord_components",
    version=version,
    author="kiki7000",
    author_email="devkiki7000@gmail.com",
    description="An unofficial library for discord components.",
    include_package_data=True,
    install_requires=["discord.py", "aiohttp"],
    license="MIT License",
    long_description=open("README.md", encoding="utf-8").read(),
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
