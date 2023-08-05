import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='cgstatistical',  
     version='0.0.3',
     author="Dimmy Magalhaes",
     author_email="dimmyk@gmail.com",
     description="CBio-Gres Statistical Tests",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/dimmykarson/CGStatistic",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )