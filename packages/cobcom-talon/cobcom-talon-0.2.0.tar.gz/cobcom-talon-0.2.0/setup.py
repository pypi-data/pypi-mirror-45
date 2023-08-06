# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    author='Samuel Deslauriers-Gauthier, Matteo Frigo, Mauro Zucchelli',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    description='A Python package that implements Tractograms As Linear '
                'Operators in Neuroimaging',
    install_requires=['numpy', 'pyunlocbox', 'scipy'],
    name='cobcom-talon',
    packages=['talon'],
    python_requires='>=3',
    url='https://gitlab.inria.fr/cobcom/talon',
    version='0.2.0',
)
