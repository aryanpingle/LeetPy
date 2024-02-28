import os
import shutil
from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

with open("version.txt", "r") as f:
    version = f.read()

# Delete directory 'leetpy.egg-info'
egg_dir = "leetpy.egg-info"
if os.path.isdir(egg_dir):
    shutil.rmtree(egg_dir)

setup(
    name="leetpy",
    version=version,
    description="A package that shows you the correct solutions for every question, gives you a suite of testcases, and lets you build your own.",
    packages=["leetpy", *find_packages(where="leetpy")],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Aryan Pingle",
    author_email="realaryanpingle@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires=">=3.8",
    keywords=[],
    project_urls={
        "homepage": "https://github.com/aryanpingle/LeetPy",
        "source": "https://github.com/aryanpingle/LeetPy",
        "download": "https://pypi.org/project/leetpy/#files",
        "tracker": "https://github.com/aryanpingle/LeetPy/issues",
    },
    package_data={"leetpy": ["info/*"]},
)
