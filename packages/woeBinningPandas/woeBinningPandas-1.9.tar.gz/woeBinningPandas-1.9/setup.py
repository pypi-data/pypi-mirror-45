import os
from setuptools import setup, find_packages
README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
 
setup(
    name='woeBinningPandas',
    version='1.9',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',  # example license
    description='My package from github repo.',
    long_description=README,
    url='https://github.com/V1ad98/woeBinningPandas.git',
    author='V1ad98',
    author_email='47775603+V1ad98@users.noreply.github.com',
	install_requires=['pandas','numpy'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
)