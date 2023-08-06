import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="confiy",
    version="1.3",
    author="Hasan Sajedi",
    author_email="hassansajedi@gmail.com",
    description="With this module you can easy take the value of config file only by key, in python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hasansajedi/confiy",
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests*']),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)