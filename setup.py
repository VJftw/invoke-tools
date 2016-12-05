
"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
from os import path
from subprocess import check_output
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

version = check_output('git describe --abbrev=0'.split(' ')).decode(
    'utf-8').strip()

setup(
    name='invoke-tools',

    version=version,

    description='A set of tools to use the Invoke task runner easier in a work-flow.',
    url='https://github.com/VJftw/invoke-tools',
    author='VJ Patel',
    author_email='vj@vjpatel.me',
    license='MIT',
    zip_safe=False,

    packages=find_packages(),
    install_requires=['docker-py', 'invoke', 'psutil', 'py-cpuinfo', 'gitpython', 'requests'],
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

    keywords='invoke tools'
)
