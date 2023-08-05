import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='goku',
     version='0.2',
     scripts=['goku.py'] ,
     author="Jatin Pandey",
     author_email="jatinpandeywork@gmail.com",
     description="A Super Sayaian  package KAAAA__MAEEE--HAA__MAEE_HAAAAAA",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/Jatin543/mypackage1",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
