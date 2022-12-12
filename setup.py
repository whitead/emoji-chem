from glob import glob

from setuptools import setup

exec(open("emojichem/version.py").read())

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="emojichem",
    version=__version__,
    description="Replace elements with emojis in rdkit",
    author="Andrew White",
    author_email="andrew.white@rochester.edu",
    url="https://github.com/whitead/emojichem",
    license="MIT",
    packages=["emojichem"],
    install_requires=["rdkit"],
    test_suite="tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
