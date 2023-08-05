#!/usr/bin/env python

from distutils.core import setup
import setuptools

setup(name='iris_python_client',
      version='0.1',
      description='Iris message bus',
      author="John Root",
      author_email="john.root@digirati.com",
      url='https://github.com/digirati-co-uk/iris4py',
      packages=setuptools.find_packages(),
      license='MIT',
      install_requires=[
          'boto3'
      ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          "Programming Language :: Python :: 3",
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ]
      )
