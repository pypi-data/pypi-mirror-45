from setuptools import setup, find_packages
from os.path import join, dirname

setup(name='woeBinningPandas',
      version='1.6',
      description='My package from github repo',
      long_description=open(join(dirname(__file__), 'README.md')).read(),
	  long_description_content_type='text/markdown',
      url='https://github.com/V1ad98/woeBinningPandas.git',
      author='V1ad98',
      author_email='47775603+V1ad98@users.noreply.github.com',
      license='MIT',
      packages=find_packages(),
      install_requires=['markdown', 'pandas', 'numpy'],
	  )