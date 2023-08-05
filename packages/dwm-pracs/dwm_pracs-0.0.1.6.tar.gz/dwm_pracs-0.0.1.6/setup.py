import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dwm_pracs",
    version="0.0.1.6",
    author="VRMB",
    description="dwm-pracs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bhushan-borole/dwm-pracs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

