#coding=utf8
__author__ = 'liming'

from setuptools import setup

setup(name='table2excel',
      version='0.0.1',
      description='Dump Table (List in List) to an excel file',
      url='https://github.com/theatoken/table2excel',
      author='Alexander.Li',
      author_email='superpowerlee@gmail.com',
      license='MIT',
      packages=['table2excel'],
      install_requires=[
          'xlwt',
      ],
      zip_safe=False)