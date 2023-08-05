from setuptools import setup, find_packages

setup(
  name='cjkitchehelloworld',
  version='0.0.4',
  description='Test package',
  package_dir={'': 'src'},
  packages=find_packages('src'),
  install_requires=[
    'Click'
  ],
  entry_points='''
    [console_scripts]
    helloworld=__main__:cli
  '''
)