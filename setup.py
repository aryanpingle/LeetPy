import os
import shutil
from setuptools import find_packages, setup
from packaging.version import Version
from rich import print as rich_print

with open("README.md", "r") as f:
    long_description = f.read()

with open("version.txt", "r") as f:
    version = f.read()

version = "0.1.0"

# Validate the version name
try:
    v = Version(version)
    rich_print(f"[bold cyan]{version}[/] [bold green]is a valid version name[/]")
except:
    rich_print(f"[bold cyan]{version}[/] [bold red]is not a valid version name[/]")
    exit(1)

# Delete directory 'leetpy.egg-info'
egg_dir = "leetpy.egg-info"
if os.path.isdir(egg_dir):
    shutil.rmtree(egg_dir)

setup(
    name="leetpy",
    version=version,
    description="A package that shows you the correct solutions for every question, gives you a suite of testcases, and lets you build your own.",
    packages=["leetpy", *["leetpy." + i for i in find_packages(where="leetpy")]],
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
    install_requires=["rich>=13.7.1"],
    python_requires=">=3.8",
    keywords=[],
    project_urls={
        "Homepage": "https://github.com/aryanpingle/LeetPy",
        "Source": "https://github.com/aryanpingle/LeetPy",
        "Download": "https://pypi.org/project/leetpy/#files",
        "Tracker": "https://github.com/aryanpingle/LeetPy/issues",
    },
    package_data={"leetpy": ["info/*"]},
)
