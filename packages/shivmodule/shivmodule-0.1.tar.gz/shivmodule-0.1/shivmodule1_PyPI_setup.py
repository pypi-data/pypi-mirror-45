#!/usr/bin/env python

from distutils.core import setup

# This setup is suitable for "python setup.py develop"

setup(name='shivmodule',
      version='0.1',
      description='A silly math package',
      author='Shivprasad Parab',
      author_email='parabos2001@yahoo.com',
      url='http://www.google.com/',
      packages=['shivmodule', 'shivmodule.adv'],
      )

