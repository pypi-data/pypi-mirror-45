import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "example-pkg-VamsiKrishnaMeda",
    version = "0.0.1",
    author = "Vamsi Krishna",
    author_email = "medav1@mymail.nku.edu",
    description = "A small example package",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)