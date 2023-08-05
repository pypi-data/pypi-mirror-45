from setuptools import setup
import os
import gitbump as pkg

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
else:
    version = os.environ.get('CI_JOB_ID', '0.0.0')

setup(name=pkg.__name__,
      version=version,
      description='Git tags version automation',
      url='https://gitlab.com/w00/gitbump',
      author='Lukasz Kwiek',
      include_package_data=True,
      py_modules=[pkg.__name__],
      author_email='lukasz.kwiek@ericsson.com',
      license='MIT',
      entry_points={
          'console_scripts': ['{name}={name}:main'.format(name=pkg.__name__)]
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: MIT License',  # Again, pick a license
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5'
      ],
      install_requires=['semver==2.8.1'])
