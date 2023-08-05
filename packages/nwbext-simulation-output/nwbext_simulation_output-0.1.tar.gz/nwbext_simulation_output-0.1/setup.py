from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nwbext_simulation_output',
    version='0.1',
    description='Extension for storing large-scale simulation output in the Neurodata Without Borders: Neurophysiology format',
    long_description=long_description,
    author='Ben Dichter',
    author_email='ben.dichter@gmail.com',
    keywords=['nwb', 'extension'],
    packages=find_packages(),
    install_requires=['pynwb', 'hdmf', 'numpy'],
    # the last two lines ensure that pip installation includes the yaml files
    package_data={'': ['simulation_output.namespace.yaml',
                       'simulation_output.extensions.yaml']},
    include_package_data=True,
    #entry_points={'pynwb.extensions': 'simulation_output = nwbext_simulation_output'},
)
