# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 19:20:21 2019

@author: Lenovo
"""

from setuptools import setup,find_packages

setup(name='contextualMAB',
      version='0.2',
      description='Modules for solving contextual Multi arm bandit problems',
      url='http://github.com/karthickrajas/contextualMAB',
      author='Karthick Raja',
      author_email='karthick11b36@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['numpy','pandas','matplotlib'],
      zip_safe=False)