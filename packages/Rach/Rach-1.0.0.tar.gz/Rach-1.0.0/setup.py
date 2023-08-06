import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Rach",
    version="1.0.0",
    author="srinskit",
    author_email="srinskit.off@gmail.com",
    description="Python client for Rach",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/srinskit/RachPy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
