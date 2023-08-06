import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Print-o-box--PyCoderBoi",
    version="0.0.1",
    author="PyCoderBoi",
    author_email="bluejayy350@yahoo.com",
    description="a little playground for printing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PyCoderBoi/print-o-box",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
