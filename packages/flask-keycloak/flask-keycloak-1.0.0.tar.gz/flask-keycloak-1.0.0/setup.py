# -*- coding: utf-8 -*-
from setuptools import find_packages, setup


setup(
    name='flask-keycloak',
    version='1.0.0',
    description='flask integration with keycloak',
    url='https://github.com/akhilputhiry/flask-keycloak',
    author='Akhil Lawrence',
    author_email='akhilputhiry@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3.6'
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'keycloak==1.6.0',
    ],
)
