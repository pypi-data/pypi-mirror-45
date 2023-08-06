import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phone-operator-recognizer",
    version="0.0.1",
    author="Artem Nester",
    author_email="artem.nester.m@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nsefh/operator-detector-by",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)