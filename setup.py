import sys
import os

from setuptools import setup, find_packages


version = '0.4'

setup(name='nose-selecttests',
      version=version,
      description="Specify whitelist of keywords for tests to be run by nose",
      long_description="""""",
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
      ],
      entry_points={
          'nose.plugins.0.10': [
                'selecttests = noseselecttests:NoseSelectPlugin'
          ]
      },
)
