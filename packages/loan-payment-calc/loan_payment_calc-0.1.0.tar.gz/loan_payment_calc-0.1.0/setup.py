from setuptools import setup, find_packages

import unittest
def unit_test():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_loans.py')
    return test_suite

unit_test()

try:
    import pypandoc
    long_descr = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_descr = open('README.md').read()

setup(name='loan_payment_calc',
      version='0.1.0',
      description='Loan payment calculator',
      long_description=long_descr,
      classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
      ],
      keywords='loan',
      author='Tyler Norlund',
      author_email='t_norlund@u.pacific.edu',
      license='MIT',    
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      test_suite='tests',
      include_package_data=True,
      zip_safe=False)