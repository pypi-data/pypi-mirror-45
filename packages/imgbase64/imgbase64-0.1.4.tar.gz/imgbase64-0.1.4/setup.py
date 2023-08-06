# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='imgbase64',
    version='0.1.4',
    url='https://github.com/Ronnasayd/imgbase64',
    license='MIT License',
    author='Ronnasayd de Sousa Machado',
    author_email='ronnasayd@hotmail.com',
    keywords='image bas64 url',
    description=u'Transforma images em base64',
    long_description=u'''Transforma images em base64''',
    packages=['imgbase64'],
    install_requires=['argparse', 'requests'],
)
