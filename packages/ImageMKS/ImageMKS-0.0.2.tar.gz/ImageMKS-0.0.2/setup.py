from distutils.core import setup
from setuptools import find_packages

setup(
    name='ImageMKS',
    version='0.0.2',
    packages=find_packages(),
    license='The MIT License (MIT)',
    long_description=open('README.md').read(),
    author='Sven Voigt',
    author_email='svenpvoigt@gmail.com',
    url='http://pypi.python.org/pypi/ImageMKS/',
    description='Sharing segmentation frameworks.',
    install_requires=[],
)
