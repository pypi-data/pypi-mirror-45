import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="defender",
    version="0.0.3",
    author="QuantumBlack Labs",
    author_email="opensource@quantumblack.com",
    description="defender",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://quantumblack.com/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    license="Apache 2.0",
)
