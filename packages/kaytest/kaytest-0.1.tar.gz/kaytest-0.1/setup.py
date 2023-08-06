import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='kaytest',
    version='0.1',
    author="Amr Kayid",
    author_email="amrkayid2027@gmail.com",
    description="Kayid's first python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amrmkayid/kaytest",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)
