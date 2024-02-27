from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name = "leetpy",
    version = "0.0.1",
    description = "A package that shows you the correct solutions for every question, gives you a suite of testcases, and lets you build your own.",
    package_dir = {"": "src"},
    packages = find_packages(where="src"),
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/aryanpingle",
    author = "Aryan Pingle",
    author_email = "realaryanpingle@gmail.com",
    license = "MIT",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires = [],
    extras_require = {
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires = ">=3.8",
)
