import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-norbinsh",
    version="0.0.2",
    author="Shay Elmualem",
    author_email="wowshay@gmail.com",
    description="A very empty example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://example.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)