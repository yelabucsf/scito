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
            'seaborn',
            'matplotlib',
            'pandas',
            'scikit-learn',
            'scipy',
            'statsmodels',
            'Click'
      ],
      entry_points='''
      [console_scripts]
      scito=scito.cli:cli		
      ''',
      ext_modules=[Extension('cmath11', ['src/test.c'])],
      include_package_data=True,
      zip_safe=False)
