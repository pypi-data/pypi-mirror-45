import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytorchfi",
    version="0.1.2",
    author="UIUC RSim",
    description="A runtime fault injector for PyTorchFI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pytorchfi/pytorchfi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
