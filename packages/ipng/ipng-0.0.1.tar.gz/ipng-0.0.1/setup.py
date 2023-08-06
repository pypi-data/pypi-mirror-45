import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ipng",
    version="0.0.1",
    author="hanjoes",
    author_email="hanzhou87@gmail.com",
    description="Intuitive PNG library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hanjoes/ipng",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)