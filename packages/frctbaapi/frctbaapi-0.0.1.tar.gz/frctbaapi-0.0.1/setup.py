import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="frctbaapi",
    version="0.0.1",
    author="Kyle Preiksa",
    author_email="preiksa.kyle@gmail.com",
    description="A package to interface with The Blue Alliance API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kpreiksa/TBApy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)