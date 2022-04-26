from setuptools import setup, find_packages


import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name="papflix-package-kpaparid",
    version="0.0.26",
    author="kpaparid",
    author_email="kpaparid@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.6",

)