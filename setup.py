
"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='invoke-docker-flow',

    version='0.0.1',

    description='A small set of tools to make using Docker with the Invoke task runner easier. Also incorporates a Flow system for use with git-flow.',
    url='https://github.com/VJftw/invoke-docker-flow',
    author='VJ Patel',
    author_email='vj@vjpatel.me',
    license='MIT',
    zip_safe=False,

    packages=['idflow'],
    install_requires=['docker-py', 'invoke', 'psutil', 'py-cpuinfo'],
    extras_require={
    'test': ['nose', 'coverage', 'rednose']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='invoke docker flow'
)
