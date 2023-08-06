import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sghmcmc",
    version="0.2.6",                        # Update this for every new version
    author="Xiaoyu Jiang & Luman Huang",
    author_email="xj35@duke.edu",
    description="long description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[                      # Add project dependencies here
        "pandas>=0.20.0",
        'numpy>=1.8.1',
        'scipy>=0.14.1',
        "numba",
        "multiprocess"                  # example: pandas version 0.20 or greater                          
    ],                                             
    url="https://github.com/jiangxiaoyuww/sghmc-",  
    packages=setuptools.find_packages(),
    classifiers=(                                 # Classifiers help people find your 
        "Programming Language :: Python :: 3",    # projects. See all possible classifiers 
        "License :: OSI Approved :: MIT License", # in https://pypi.org/classifiers/
        "Operating System :: OS Independent",   
    ),
)

