import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="papagei-niederha",
    version="0.0.2",
    author="Niederhauser Loïc",
    author_email="loic.niederhauser@gmail.com",
    description="A package for easy verbose logging, error and warnings.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/niederha/papagei",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)