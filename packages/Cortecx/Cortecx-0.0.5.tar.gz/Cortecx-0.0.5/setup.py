import sys, os
from setuptools import setup, find_packages

version = '0.0.5'

setup(name='Cortecx',
      version=version,
      description="Cortecx is a NLP library",
      long_description=open('README.md').read(),
      classifiers=[],
      keywords='artificial intelligence',
      author='Lleyton Ariton',
      author_email='lleyton.ariton@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      )
