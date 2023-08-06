#!/user/bin/env python
#!-*- coding:utf-8 -*-
'''
Created on 20190506
@auther: dq
'''
from setuptools import setup,find_packages
setup(name = 'kdbase',
      version= '1.1',
      keywords = ('pip', 'kdbase', 'featureextraction'),
      description = 'Custom script',
      license = 'MIT Licence',
      url = 'http://duquan@git.kuandeng.com/scm/~duquan/kdbase.git',
      author = 'dq',
      author_email = 'duquan@kuandeng.com',
      packages = find_packages(),
      include_package_data = True,
      platforms = "any"
      #packages = ['kd_infra'],
     )
