import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(
    

    name='KSULasso_Python',  

    version='0.2',

    scripts=['KSULasso'],

    author="Sams Khan",

    author_email="ssamskhann@gmail.com",

    description="Lasso Algorithm",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://github.com/samskhan/KSULasso",

    packages=setuptools.find_packages(),

    classifiers=[

        "Programming Language :: Python :: 3",

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

    ],

)
