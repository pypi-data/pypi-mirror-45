import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brix",
    version="0.1",
    author="Nikos Tsaou",
    author_email="ntsaoussis@gmail.com",
    description="Brix is a library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tsanikgr/brix",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

