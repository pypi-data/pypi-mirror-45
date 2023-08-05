"""
.. Dstl (c) Crown Copyright 2019
"""
from setuptools import setup, find_packages

def readme():
      with open('README.md') as in_file:
            return ''.join(l for l in in_file if '![' not in l)


setup(name='noisify',
      version='1.0',
      description='Framework for creating synthetic data with realistic errors for refining data science pipelines.',
      url='https://github.com/dstl/Noisify',
      long_description=readme(),
      long_description_content_type='text/markdown',
      author='Declan Crew',
      author_email='dcrew@dstl.gov.uk',
      license='MIT',
      packages=find_packages(),
      install_requires=[],
      test_suite='noisify.tests',
      test_requires=['numpy', 'Pillow', 'pandas'])
