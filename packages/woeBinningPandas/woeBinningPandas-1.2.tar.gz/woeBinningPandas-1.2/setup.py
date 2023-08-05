from setuptools import setup,find_packages

setup(
    name='woeBinningPandas',
    version='1.2',
    description='My package from github repo',
    url='https://github.com/V1ad98/woeBinningPandas.git',
    author='V1ad98',
    author_email='47775603+V1ad98@users.noreply.github.com',
    license='unlicense',
    packages=find_packages(),
    zip_safe=False,
    install_requires=['pandas', 'numpy']

)