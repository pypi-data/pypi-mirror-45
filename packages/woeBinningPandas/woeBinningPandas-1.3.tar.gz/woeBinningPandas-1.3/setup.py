from setuptools import setup, find_packages

setup(name='woeBinningPandas',
      version='1.3',
      description='My package from github repo',
      long_description='My package from github repo',
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