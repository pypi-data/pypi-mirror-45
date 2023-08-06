# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

install_requires = [
    'matplotlib==3.0.2',
    'pyserial==3.4',
    'numpy==1.16.1'
]

setup(
    name='transvenous_pacing_gui',
    version='0.7.6',
    description='Transvenous pacing procedure simulation GUI written in Python 3',
    long_description=readme,
    author='Nam Tran, Cooper Pearson, Richie Beck, Marcel Isper, Brianna Cathey',
    author_email='tranngocnam97@gmail.com',
    url='https://github.com/omn0mn0m/transvenous_pacing_gui',
    license="MIT license",
    packages=find_packages(exclude=('tests', 'docs')),
    tests_require=['pytest'],
    extras_require={
        'testing': ['pytest'],
    },
    scripts=['bin/transvenous_pacing_gui'],
    install_requires=install_requires,
)
