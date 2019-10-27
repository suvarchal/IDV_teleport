from codecs import open
from setuptools import setup
import os


setup( 
    name='idv_teleport',
    version='1.70',
    url="https://github.com/suvarchal/IDV_teleport",
    author='Suvarchal',
    author_email='suvarchal.kumar@gmail.com',
    license="MIT",
    description="IDV scripts to teleport bundles",
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    install_requires=['requests'],
    scripts=['bin/idv_teleport'],
    classifiers=[
    'Development Status :: 4 - Beta',

    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
]
)

