from setuptools import setup, find_packages

import unittest

def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite

my_test_suite()

try:
  import pypandoc
  long_descr = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
  long_descr = open('README.md').read()

setup(
    name='MinimumValue',
    version='0.1.0',
    description='Using gradient descent to find a value  which minimizes the function',
    long_description=long_descr,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    keywords='GradientDescent',
    author='Golnaz Abrishami',
    author_email='g_abrishamiosgoui@u.pacific.edu',
    license='MIT',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=['pandas', 'numpy','sympy'],
    test_suite='tests',
    include_package_data=True,
    zip_safe=False

)