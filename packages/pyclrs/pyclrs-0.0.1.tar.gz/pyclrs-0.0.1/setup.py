import setuptools


with open('README.md', "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyclrs",
    version="0.0.1",
    author="Oliven",
    author_email="Liuhedong135@163.com",
    description="Print color on Linux or Windows terminals.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liuhedong135/pyclrs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)