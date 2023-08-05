import os
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(name='mongo_pickle',
      version='0.1.6',
      description='Schema-less Pythonic Mongo ORM',
      long_description=readme,
      author='111yoav',
      author_email='111yoav@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=False)
