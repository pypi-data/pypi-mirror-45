import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('LICENSE') as f:
    license = f.read()

setuptools.setup(
    name="bpf2eaf",
    version="0.0.5",
    author="Thomas Kisler",
    author_email="kisler@bas.uni-muenchen.de",
    description="Package converting bpf to eaf.",
    license=license,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
