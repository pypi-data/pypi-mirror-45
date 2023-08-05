from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='RoboBoto3',
    version='1.0.0',
    packages=[''],
    package_dir={'': 'roboboto3'},
    url='https://www.github.com/we45/RoboBoto3',
    license='MIT',
    author='we45',
    author_email='info@we45.com',
    description='Utility functions for Robot Framework Security libs' ,
    install_requires=[
        'robotframework',
        'boto3'
    ],
    long_description = long_description,
    long_description_content_type='text/markdown'
)
