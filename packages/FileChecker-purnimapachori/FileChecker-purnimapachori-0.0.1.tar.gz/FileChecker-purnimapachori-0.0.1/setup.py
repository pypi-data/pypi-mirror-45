import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FileChecker-purnimapachori",
    version="0.0.1",
    author="Purnima Pachori",
    author_email="purnima.pachori@quadram.ac.uk",
    description="A package to investigate a directory for cleanup",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pachorip/file_investigation",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
