from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()
 

setup( 
    name='idv_teleport',
    version='1.2',
    url="https://github.com/suvarchal/IDV_teleport",
    author='Suvarchal',
    author_email='suvarchal.kumar@gmail.com',
    license="MIT",
    description="IDV scripts to teleport bundles and publish to ramadda",
    #long_description=read('README.md'),
    scripts=['bin/idv_teleport','bin/ramadda_publish'],
    classifiers=[
    'Development Status :: 4 - Beta',

    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Framework :: IPython',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
]
)

