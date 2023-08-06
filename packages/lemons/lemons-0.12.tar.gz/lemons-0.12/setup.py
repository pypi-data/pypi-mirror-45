import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
     name='lemons',
     version='0.12',
     author="Jake Brehm",
     author_email="mail@jakebrehm.com",
     description="A GUI and common function utility package",
     long_description=README,
     long_description_content_type="text/markdown",
     url="https://github.com/jakebrehm/lemons",
     packages=find_packages(),
     include_package_data=True,
     classifiers=[
         "Programming Language :: Python :: 3",
         "Programming Language :: Python :: 3.7",
         "Operating System :: OS Independent",
     ],
 )
