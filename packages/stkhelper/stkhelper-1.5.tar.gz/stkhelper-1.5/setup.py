from setuptools import setup, find_packages

info = open('README.md').read()

setup(
      name='stkhelper',
      version='1.5',
      description='Uses the STK software to create simulations for satellite testing',
      long_description=info,
      author='W. Conor McFerren',
      author_email='cnmcferren@gmail.com',
      url="https://github.com/cnmcferren/stkhelper",
      packages=find_packages(),
      install_requires=[
          'comtypes',
          'pypiwin32']
)
