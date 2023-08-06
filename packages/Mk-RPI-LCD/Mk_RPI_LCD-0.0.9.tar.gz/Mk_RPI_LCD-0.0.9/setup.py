import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Mk_RPI_LCD",
    version="0.0.9",
    author="Mark Cartagena",
    author_email="mark@mknxgn.com",
    description="Raspberry pi SDA/SSCL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://mknxgn.com/",
    install_requires=[
        'mknxgn_essentials'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
