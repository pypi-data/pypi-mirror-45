from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["ipython>=6", "nbformat>=4", "nbconvert>=5", "requests>=2"]

setup(
    name="demopippack",
    version="0.0.1",
    author="Safal Sigdel",
    author_email="safalsigdel@gmail.com",
    description="A Simple pip package ",
    long_description=readme,
    url="https://github.com/safal321/demopippack.git",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
