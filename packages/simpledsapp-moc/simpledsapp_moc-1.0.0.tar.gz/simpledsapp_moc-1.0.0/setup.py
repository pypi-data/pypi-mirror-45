import sys
import os
# Make sure we are running python3.5+
if 10 * sys.version_info[0]  + sys.version_info[1] < 35:
    sys.exit("Sorry, only Python 3.5+ is supported.")

from setuptools import setup


def readme():
    print("Current dir = %s" % os.getcwd())
    print(os.listdir())
    with open('README.rst') as f:
        return f.read()

setup(
      name             =   'simpledsapp_moc',
      version          =   '1.0.0',
      description      =   'A simple DS type ChRIS application specifically created for the Massachusetts Open Cloud remote computing environment.', 
      long_description =   readme(),
      author           =   'FNNDSC',
      author_email     =   'dev@babyMRI.org',
      url              =   'http://wiki',
      packages         =   ['simpledsapp_moc'],
      install_requires =   ['chrisapp', 'pudb'],
      test_suite       =   'nose.collector',
      tests_require    =   ['nose'],
      scripts          =   ['simpledsapp_moc/simpledsapp_moc.py'],
      license          =   'MIT',
      zip_safe         =   False
     )
