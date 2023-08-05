import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sifima",
    version="0.24",
    author="Gerod",
    author_email="maksd241@gmail.com",
    description="This is a project to work with files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gerod220/sifima",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)