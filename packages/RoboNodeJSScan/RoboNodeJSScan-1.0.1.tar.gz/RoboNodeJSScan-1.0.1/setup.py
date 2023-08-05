from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='RoboNodeJSScan',
    version='1.0.1',
    packages=[''],
    package_dir={'': 'robonodejsscan'},
    url='https://www.github.com/we45/RoboNodeJSScan',
    license='MIT',
    author='we45',
    author_email='info@we45.com',
    description='Robot Framework Library for NodeJSScan SAST Scanner' ,
    install_requires=[
        'docker',
        'robotframework==3.0.4',
        'requests'
    ],
    long_description = long_description,
    long_description_content_type='text/markdown'
)
