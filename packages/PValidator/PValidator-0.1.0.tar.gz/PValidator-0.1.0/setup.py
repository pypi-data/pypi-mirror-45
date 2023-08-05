import setuptools
#with open("README.md", "r") as fh:
 #   long_description = fh.read()

#packaging
setuptools.setup(
    name="PValidator",
    version="0.1.0",
    author="Itay Bardugo",
    author_email="itaybardugo91@gmail.com",
    description="Pvalidaor provides general validations for the given class",
    long_description="Pvalidaor provides general validations for the given class",
    long_description_content_type="text/markdown",
    #url="https://github.com/itay-bardugo/prsync/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
