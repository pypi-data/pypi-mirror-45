from setuptools import setup, find_packages

from os import path
# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(name='woeBinningPandas',
      version='1.4',
      description='My package from github repo',
      long_description=long_description,
	  long_description_content_type='text/markdown',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='Package from github repo',
      url='https://github.com/V1ad98/woeBinningPandas.git',
      author='V1ad98',
      author_email='47775603+V1ad98@users.noreply.github.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['markdown', 'pandas', 'numpy'],
      include_package_data=True,
      zip_safe=False)