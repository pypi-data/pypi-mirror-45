# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='flylog2',
      version='0.1.80',
      description='make log fly to mail or other',
      author='grey',
      author_email='greyeee@gmail.com',
      url='https://github.com/dantezhu/flylog',
      packages=find_packages(),
      install_requires=['requests', 'telegram==0.0.1', 'python-telegram-bot==11.1.0'],
)
