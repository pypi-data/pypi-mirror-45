import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pi7447",
    version="1.0.0",
    author="Philip Huang",
    author_email="p208p2002@gmail.com",
    description="7447 lib for raspberry pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/p208p2002/pi7447",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)