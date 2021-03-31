from setuptools import setup, find_packages
from distutils.core import setup, Extension


setup(name='scito',
      version='0.2.0',
      description='YeLab software to perform SCITO-seq analysis',
      url='https://github.com/yelabucsf/scito',
      author='Anton Gvaihir Ogorodnikov, Ye Lab UCSF',
      author_email='anton.ogorodnikov@ucsf.edu',
      license='GNU V3',
      packages=find_packages(),
      install_requires=[
            'numpy',
            'boto3',
            'ufixtures @ git+https://github.com/Gvaihir/ufixtures#egg=ufixtures'
      ],
      include_package_data=True,
      zip_safe=False)
