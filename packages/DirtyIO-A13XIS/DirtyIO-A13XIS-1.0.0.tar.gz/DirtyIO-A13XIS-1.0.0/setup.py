import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DirtyIO-A13XIS",
    version="1.0.0",
    author="Lex Sternin",
    author_email="allseeingstar@googlemail.com",
    description="Dirty quick binary file management library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/A13XIS/dirtyio",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)