# coding=utf-8
# Author: Yongwei
# @Time: 19-4-19 下午4:16

from distutils.core import setup
from setuptools import find_packages

setup(name='theagao',
      version='2019.4.19',
      description='this is the 1st version',
      long_description='',
      author='theagao',
      author_email='',
      url='',
      license='',
      install_requires=['librosa',
                   'numpy'],
      classifiers=[
                   'Programming Language :: Python :: 2.7'],
      keywords='',
      packages=find_packages('src'),  # 必填
      package_dir={'': 'src'},  # 必填
      include_package_data=True,
      )
