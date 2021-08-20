from os import environ
from setuptools import setup, find_packages

try:
    version = (
        environ["TRAVIS_TAG"].lstrip("v")
        if environ["TRAVIS"] == "true"
        else environ["VERSION_NUMBER"]
    )
except KeyError:
    version = tempversion

setup(
    name='discord-components',
    version='some version',
    license='a licence',
    author='plun1331',
    author_email="devkiki7000@gmail.com",
    description="An unofficial library for discord components (under-development)",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kiki7000/discord.py-components",
    packages=find_packages(),
    install_requires=open("requirements.txt").readlines(),
    python_requires=">=3.7",
)
