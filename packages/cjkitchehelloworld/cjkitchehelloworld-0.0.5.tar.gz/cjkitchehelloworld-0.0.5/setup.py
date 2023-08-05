from setuptools import setup, find_packages

setup(
  name='cjkitchehelloworld',
  version='0.0.5',
  description='Test package',
  package_dir={'': 'src'},
  packages=find_packages('src'),
  install_requires=[
    'Click'
  ],
  entry_points={
    'console_scripts': [
      'helloworld = cfn.__main__:main'
    ]
  }
)