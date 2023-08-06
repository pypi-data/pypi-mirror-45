import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libenum",
    version="1.0.0",
    author="Xue Jiao",
    author_email="jiao.xuejiao@gmail.com",
    description="A small enum package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/caser789/libenum",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['six'],
)
