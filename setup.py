from setuptools import setup
import os

version = {}
with open('version.py') as fp:
    exec(fp.read(), version)
version = version["__version__"]


setup(name='akeneo-api',
      version=version,
      description='Akeneo API Client',
      url='https://github.com/joshmuente/akeneo-api',
      author='Josh Münte',
      author_email='josh.muente@flagbit.de',
      license='MIT',
      packages=['akeneoapi'],
      zip_safe=False,
      install_requires=[
          'urllib3==1.26.6',
          'pandas==1.3.3',
          'rest3client==0.3.4',
          'streamlit==0.88.0'
      ])
