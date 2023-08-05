import setuptools 

with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="example_pkg_1203-prteek",
    version="0.0.1",
    author="Prateek",
    author_email="iprtk@icloud.com",
    description="First trial with packaging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free For Home Use",
        "Operating System :: OS Independent",
    ],
)
