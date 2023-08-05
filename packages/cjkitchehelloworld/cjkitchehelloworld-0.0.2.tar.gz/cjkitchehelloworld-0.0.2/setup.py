from setuptools import setup, find_packages


setup(
  name='cjkitchehelloworld',
  version='0.0.2',
  packages=find_packages(),
  install_requires=[
    'Click'
  ],
  entry_points='''
    [console_scripts]
    helloworld=cli:main
  '''
)