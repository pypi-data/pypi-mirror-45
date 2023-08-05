from setuptools import setup

with open('README.txt') as file:
    long_description = file.read()

setup(name='firedb',
      version='0.1',
      description='Google Cloud FireStore Database Utilities - Backup, Restore, Import, List',
      long_description=long_description,
      url='https://github.com/ipal0/firedb',
      author='Pal',
      author_email='ipal0can@gmail.com',
      license='GPL',
      python_requires='>=3',
      packages=['firedb'])
