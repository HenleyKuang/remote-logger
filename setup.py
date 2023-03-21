# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()


setup(
    name='remote-logger',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version='0.3.2',

    description='Remote Logger',
    long_description_content_type='text/x-rst',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/HenleyKuang/remote-logger',

    # Author details
    author='Henley Kuang',
    author_email='hekuang@ucdavis.edu',

    # Choose your license
    license='GPL',
    # See https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=[

        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
    # What does your project relate to?
    keywords='python logger ',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(
        exclude=['contrib', 'docs', 'tests*', 'playground*', 'img']),

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/technical.html#install-requires-vs-requirements-files
    python_requires=">=3.6",
    install_requires=[
        'google-cloud-logging==1.12.1',
        'sentry-sdk==1.14.0'
    ],
)
