import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read() 

setuptools.setup(
     name='pyrateek',
     version='0.2',
     scripts=['pyrateek'] ,
     author="Prateek",
     author_email="iprtk@icloud.com",
     description="Desperate attempt at a utility package",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
