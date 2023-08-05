import setuptools
# from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nifverifier",
    version="0.0.1",
    author="Charlie Brown",
    author_email="bruno11.francisco@gmail.com",
    description="Simple package to verify and generate NIF numbers in Portugal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CharlieBrownCharacter/nifverifier",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
