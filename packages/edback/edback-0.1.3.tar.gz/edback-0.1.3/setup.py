import setuptools
from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    url='https://moreal.kr/~edback',
    name='edback',
    version='0.1.3',
    long_description=long_description,
    description='Simple encrypt, decrypt, backup console application',
    author='moreal',
    author_email='dev.moreal@gmail.com',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'pycrypto',
    ],
    entry_points='''
        [console_scripts]
        edback=edback.cli:cli
    ''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX',
        'Topic :: Utilities'
    ]
)