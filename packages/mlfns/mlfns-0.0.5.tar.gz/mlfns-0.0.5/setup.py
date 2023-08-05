"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()
    

setup(
  name="mlfns",      # $ pip install ml_pyfns
  # PEP0440 compatible formatted version, see:
  # https://www.python.org/dev/peps/pep-0440/
  #
  # Generic release markers:
  #   X.Y
  #   X.Y.Z   # For bugfix releases
  #
  # Admissible pre-release markers:
  #   X.YaN   # Alpha release
  #   X.YbN   # Beta release
  #   X.YrcN  # Release Candidate
  #   X.Y     # Final release
  #
  # Dev branch marker is: 'X.Y.dev' or 'X.Y.devN' where N is an integer.
  # 'X.Y.dev0' is the canonical version of 'X.Y.dev'
  #
  version="0.0.5",
  description="Machine Learning Python utility functions",
  long_description=long_description,
  long_description_content_type="text/markdown",
  #url="https://github.com/gcloudex/mlfns",
  author="Explore AI for Good",
  author_email="gcloudex@gmail.com",
  packages=find_packages(exclude=['docs', 'tests']),
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  keywords='development artificial intelligent machine learning ai ml',
)