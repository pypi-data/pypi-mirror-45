import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyWrangler",
    version="0.0.2",
    author="Peter Mugenyi",
    author_email="petermugenyi@gmail.com",
    description="A python package containing some easy-to-use tools for data cleaning / Exploration and ML.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pmugenyi/PyWrangler-0.0.2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)