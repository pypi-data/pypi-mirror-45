import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hhsearch_python",
    version="1.12",
    author="Tim D.",
    author_email="",
    description="A small package to deal with HHSearch files.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MrRedPandabaer/hhsearch-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)