#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name="OpenTEA",
    version="3.0.0rc1",
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        'console_scripts': [
            'example = opentea.gui.example:main',
        ],
    },
    # scripts=[
    #     'bin/opentea'
    # ],

    install_requires=[
        'jsonschema>=2.6.0',
        'Pillow>=6.0.0',
        'h5py>=2.9.0',
        'numpy>=1.16.3',
        'PyYAML>=5.1',
    ],
    package_data={'opentea': ['gui_forms/images/*.gif']},
    # metadata
    author='Antoine Dauptain',
    author_email='coop@cerfacs.fr',
    description='Helpers tools for the setup of Scientific software',
    license="CeCILL-B",
    url='http://cerfacs.fr/opentea/',
)
