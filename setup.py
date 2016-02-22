import sys
import os

from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


version = '0.5'

setup(name='nose-selecttests',
      version=version,
      description="Specify whitelist of keywords for tests to be run by nose",
      long_description=read('README.rst') + '\n\n' +
                       read('HISTORY.rst') + '\n\n' +
                       read('LICENSE'),
      classifiers=[
      ],
      keywords='',
      author='Domen Kozar',
      author_email='domen@dev.si',
      url='http://github.com/iElectric/nose-selecttests/',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'nose',
          'six',
      ],
      entry_points={
          'nose.plugins.0.10': [
                'selecttests = noseselecttests:NoseSelectPlugin'
          ]
      },
)
