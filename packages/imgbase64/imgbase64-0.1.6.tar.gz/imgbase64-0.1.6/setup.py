# -*- coding: utf-8 -*-
from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='imgbase64',
    version='0.1.6',
    url='https://github.com/Ronnasayd/imgbase64',
    license='MIT License',
    author='Ronnasayd de Sousa Machado',
    author_email='ronnasayd@hotmail.com',
    keywords='image bas64 url',
    description=u'transform images into base64',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['imgbase64'],
    install_requires=['argparse', 'requests'],
)
