import re

pkg_file = open("shs_dataset_etl/__init__.py").read()
metadata = dict(re.findall("__([a-z]+)__\s*=\s*'([^']+)'", pkg_file))
description = open('README.md').read()

from setuptools import setup, find_packages

install_requires = ['requests']

setup(
    name='shs_dataset_etl',
    description='SHS dataset ETL.',
    packages=find_packages(),
    author=metadata['author'],
    author_email=metadata['authoremail'],
    version=metadata['version'],
    url='https://github.com/pavelnyaga/shs_dataset_etl',
    license="MIT",
    keywords="etl",
    long_description=description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    include_package_data=True,

    install_requires=[
        'setuptools',
        ] + install_requires,

    entry_points={
        'console_scripts': [
            'shs_dataset_etl = shs_dataset_etl.cli:main'
        ]
    }
)
