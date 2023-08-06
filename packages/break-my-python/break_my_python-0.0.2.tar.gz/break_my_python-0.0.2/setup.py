from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='break_my_python',
    version='0.0.2',
    description='This package tries to breaks your python interpreter, do not install it',
    long_description=long_description,
    author='Jonathan J. Helmus',
    author_email='jjhelmus@gmail.com',
    url='http://pypi.python.org/pypi/break_my_python/',
    license='LICENSE.txt',
    py_modules=['break_my_python'],
    data_files=[('/', ['break_my_python.pth'])],
    classifiers=[
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    ]
)
