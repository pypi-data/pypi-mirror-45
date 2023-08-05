from setuptools import setup

setup(name='whopy',
      version='0.1.1',
      description='Module for retrieving and parsing the WHOIS data for a domain. Supports most domains.',
      author='Andrew Shamah',
      author_email='amshamah@gmail.com',
      url='https://github.com/amshamah419/whopy',
      packages=['whopy'],
      package_dir={"whopy":"whopy"},
      package_data={"whopy": ["*.dat", "*.json"]},
      install_requires=['argparse'],
      provides=['whopy'],
      license="MIT"
     )
