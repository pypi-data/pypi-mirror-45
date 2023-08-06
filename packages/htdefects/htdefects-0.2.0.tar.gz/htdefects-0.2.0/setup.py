from setuptools import setup
from setuptools import find_packages
import os

from htdefects import __version__


with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as fr:
    long_description = fr.read()

setup(
    name='htdefects',
    version=__version__,
    description='A Python package for high-throughput DFT calculations of defects',
    long_description=long_description,
    url='https://gitlab.com/hegdevinayi/citrine-defects',
    author='Vinay Hegde',
    author_email='hegdevinayi@gmail.com',
    license='Apache License 2.0',
    packages=find_packages(exclude=['docs']),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
    ],
    keywords='DFT high-throughput defects materials',
    install_requires=[
        'six',
        'numpy',
        'pypif',
        'dfttopif',
        'dftinpgen',
        'ase',
    ],
)
