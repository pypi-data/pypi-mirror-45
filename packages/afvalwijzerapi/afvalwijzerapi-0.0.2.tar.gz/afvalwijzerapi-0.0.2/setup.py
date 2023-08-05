import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="afvalwijzerapi",
    version="0.0.2",
    author="ThaStealth",
    author_email="author@example.com",
    description="Communication package for AfvalwijzerAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thastealth/afvalwijzer-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)