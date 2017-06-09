import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as fp:
    long_description = fp.read()

setup(
    name='argskwargs',
    description="flexible container for positional and keyword arguments",
    long_description=long_description,
    version='1.0.0',
    author='Wouter Bolsterlee',
    author_email='wouter@bolsterl.ee',
    url="https://github.com/wbolster/argskwargs",
    py_modules=['argskwargs'],
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
