import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyCalculus",
    version="1.0.0",
    author="Rei-Chi Lin",
    author_email="fatalframe0719@gmail.com",
    description="Calculus using Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rickiarty/PyCalculus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
