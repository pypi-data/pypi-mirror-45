from setuptools import setup, find_packages
from codecs import open
from os import path
from io import open
import modules

setup(
    name='opsworks-cli',
    description='A simple python module to work with aws opsworks',
    url='https://github.com/chaturanga50/opsworks-cli',
    author='Chathuranga Abeyrathna',
    author_email='chaturanga50@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(),
    include_package_data=True,
    version='0.4.8',
    install_requires=[
        'boto3',
        'PTable'
    ],
    scripts=['opsworks-cli'],
    project_urls={
        'Bug Reports': 'https://github.com/chaturanga50/opsworks-cli/issues',
        'Source': 'https://github.com/chaturanga50/opsworks-cli',
    }
)
