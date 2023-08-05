import os
from typing import Dict

from setuptools import find_packages, setup


def get_long_description():
    """Get long description of the package from README."""
    with open('README.md') as f:
        return f.read()


def get_version():
    """Get version number of the package from version.py without importing core module."""
    package_dir = os.path.abspath(os.path.dirname(__file__))
    version_file = os.path.join(package_dir, 'sphinxcontrib/commonmark/version.py')

    namespace: Dict = {}
    with open(version_file, 'rt') as f:
        exec(f.read(), namespace)

    return namespace['__version__']


setup(
    name='sphinxcontrib-commonmark',
    version='0.1.0',
    url='https://github.com/tk0miya/sphinxcontrib-commonmark/',
    author='Takeshi KOMIYA',
    author_email='i.tkomiya@gmail.com',
    description='Yet another commonmark processor for Sphinx',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Utilities',
    ],
    packages=find_packages(),
    install_requires=[
        'Sphinx>=2.0',
        'pycmark'
    ],
    extras_require={
        'test': [
            'tox',
            'flake8',
            'flake8-import-order',
            'pytest',
            'mypy',
        ],
    },
    namespace_packages=['sphinxcontrib'],
)
