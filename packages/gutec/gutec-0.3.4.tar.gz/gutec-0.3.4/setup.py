import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# Installs requirements and sets the environment variable
setup(
    name='gutec',
    version='0.3.4',
    author="Michael Gutierrez",
    author_email="mike97.gutierrez@gmail.com",
    description="An Alan++ complient compiler",
    long_description=long_description,
    long_description_content_type="text/markdown",
        install_requires=['Click', 'treelib', 'BeautifulTable'],
    py_modules=['gutec.cli'],
    entry_points='''
        [console_scripts]
        gutec=gutec.cli:cli
    ''',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)