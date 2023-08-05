
PJT_TEMA = 'google'

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=f"igoogle",
    version="0.0.4",
    author="innovata sambong",
    author_email="iinnovata@gmail.com",
    description=f"innovata-google",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/innovata/igoogle",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
