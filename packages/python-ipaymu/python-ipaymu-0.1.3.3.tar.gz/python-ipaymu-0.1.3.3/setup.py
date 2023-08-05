import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='python-ipaymu',  
     version='0.1.3.3',
     author="Bayu Wardani",
     author_email="bayuwardani51@gmail.com",
     description="Integrasi iPaymu",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/BayuWardani/python-ipaymu.git",
     packages=setuptools.find_packages(),
     classifiers=[
         "Development Status :: 4 - Beta",
         "Natural Language :: Indonesian",
         "Operating System :: Microsoft :: Windows",
         "Operating System :: Unix","Operating System :: MacOS",
         "Programming Language :: Python :: 3 :: Only"
     ],
 )