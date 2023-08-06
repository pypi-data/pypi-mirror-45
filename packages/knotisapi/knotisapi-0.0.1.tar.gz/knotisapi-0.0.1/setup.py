import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="knotisapi",
    version="0.0.1",
    author="Knotis Inc.",
    author_email="seth@knotis.com",
    description="Python interface for the Knotis REST API.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/Knotis/knotisapi-py",
    packages=setuptools.find_packages(),
    install_requires=[
        'librestapi'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
