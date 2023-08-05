from setuptools import setup, find_namespace_packages


setup(
  name='cjkitchehelloworld',
  version='0.0.3',
  packages=find_namespace_packages(include=['learn_cli.*']),
  install_requires=[
    'Click'
  ],
  entry_points='''
    [console_scripts]
    helloworld=cli:main
  '''
)