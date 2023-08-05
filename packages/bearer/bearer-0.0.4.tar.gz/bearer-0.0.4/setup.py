import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bearer",
    version="0.0.4",
    author="Bearer Engineering",
    author_email="engineering@bearer.sh",
    description="Bearer Python Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bearer/bearer-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)
