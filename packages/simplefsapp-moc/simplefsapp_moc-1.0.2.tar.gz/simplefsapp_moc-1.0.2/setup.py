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
      name             =   'simplefsapp_moc',
      version          =   '1.0.2',
      description      =   'A demo/testing simplefsapp for the MOC compute environment.', 
      long_description =   readme(),
      author           =   'FNNDSC',
      author_email     =   'dev@babyMRI.org',
      url              =   'http://wiki',
      packages         =   ['simplefsapp_moc'],
      install_requires =   ['chrisapp', 'pudb'],
      test_suite       =   'nose.collector',
      tests_require    =   ['nose'],
      scripts          =   ['simplefsapp_moc/simplefsapp_moc.py'],
      license          =   'MIT',
      zip_safe         =   False
     )
