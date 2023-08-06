#!/usr/bin/env python3.7
from setuptools import setup

with open("README.md", "r") as f:
      long_description = f.read()
      f.close()

setup(name='buzzsprout',
      version='0.21',
      description='Buzzsprout Podcasts Python class',
      url='https://github.com/Harrtron/buzzsprout-python',
      author='Harley Thorne',
      author_email='harleyjthorne@gmail.com',
      long_description=long_description,
      long_description_content_type='text/markdown',
      license='MIT',
      packages=['buzzsprout'],
      python_required='>3.7',
      zip_safe=False)