import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "portus",
    version = "0.5.1",
    author = "Frank Cangialosi",
    author_email = "frankc@csail.mit.edu",
    description = "Python bindings for the Portus implementation of CCP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ccp-project/portus",
    packages=['portus'],
    classifiers = [
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Rust",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Networking"
    ],
    install_requires = ['pyportus']
)
