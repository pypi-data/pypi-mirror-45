import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="drf-response-utils",
    version="0.0.1",
    author="Bruno Rodrigues Santos",
    author_email="bruesmanbruesman@hotmail.com",
    description=description,
    long_description="A small package of utilities for Django Rest Framework",
    long_description_content_type="text/markdown",
    url="https://github.com/BRZangado/responseutils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)