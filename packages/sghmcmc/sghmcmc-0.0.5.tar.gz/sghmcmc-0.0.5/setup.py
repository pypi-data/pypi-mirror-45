import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sghmcmc",
    version="0.0.5",                        # Update this for every new version
    author="Xiaoyu Jiang",
    author_email="xj35@duke.edu",
    description="long description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[                      # Add project dependencies here
        "pandas>=0.20.0"                    # example: pandas version 0.20 or greater                          
    ],                                             
    url="https://github.com/jiangxiaoyuww/sghmc-",  
    packages=setuptools.find_packages(),
    classifiers=(                                 # Classifiers help people find your 
        "Programming Language :: Python :: 3",    # projects. See all possible classifiers 
        "License :: OSI Approved :: MIT License", # in https://pypi.org/classifiers/
        "Operating System :: OS Independent",   
    ),
)

