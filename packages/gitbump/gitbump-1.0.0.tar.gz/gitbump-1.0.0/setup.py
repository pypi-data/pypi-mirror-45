from setuptools import setup
import os

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ.get('CI_JOB_ID', 'testing')

setup(name='gitbump',
      version=version,
      description='Git tags version automation',
      url='https://gitlab.com/w00/gitbump',
      author='Lukasz Kwiek',
      author_email='spam@gmail.com',
      packages=['gitbump'],
      entry_points={
          'console_scripts': ['gitbump=gitbump.cli:main']
      },
      install_requires=['semver==2.8.1'])
