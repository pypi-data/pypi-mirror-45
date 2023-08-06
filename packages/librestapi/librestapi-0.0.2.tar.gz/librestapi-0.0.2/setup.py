import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="librestapi",
    version="0.0.2",
    author="Knotis Inc.",
    author_email="seth@knotis.com",
    description="Package provides a simple interface for implementing REST resource requests.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/Knotis/librestapi-py",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
