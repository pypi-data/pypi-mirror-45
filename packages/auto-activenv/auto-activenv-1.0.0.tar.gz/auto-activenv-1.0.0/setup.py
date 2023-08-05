
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='auto-activenv',
    author='Connor Mullett',
    description='CLI to install script that automatically' \
        'activates virtual environments',
    long_description=read('README.md'),
    keywords='virtualenv venv virtual environment automation sandbox',
    packages=['src'],
    license='MIT',
    url='https://github.com/connormullett/auto-activenv',
    install_requires = [
        'click',
    ],
    version='1.0.0',
    entry_points={
        'console_scripts': [
            'activenv=src.main:install'
        ]
    }
)

