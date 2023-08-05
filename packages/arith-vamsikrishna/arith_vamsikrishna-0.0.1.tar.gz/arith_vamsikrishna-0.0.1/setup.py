import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "arith_vamsikrishna",
    version = "0.0.1",
    author = "Vamsi Krishna Meda",
    author_email = "medav1@mymail.nku.edu",
    description = "A package to compute Prime Factors",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)