import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bayesHC",
    version="0.0.1",
    author="Ezinne Nwankwo and Jennifer Wilson",
    author_email="enwankwo17@gmail.com",
    description="A package for Bayesian Hierarchical Clustering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jennifer2010/STA-663-Bayesian-Hierarchical-Clustering.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)