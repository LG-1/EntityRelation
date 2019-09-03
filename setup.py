from setuptools import setup, find_packages
from os import path
import unittest


def EntityRelation_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('test')
    return test_suite


here = path.abspath(path.dirname(__file__))

setup(
    name='EntityRelation',
    version='1.0.2',
    description='A package to extract relations between entities. '
                'this maybe helpful and a important link for constructing KG. '
                'base on DSNF(Dependency Semantic Normal Forms) for now. ',

    # The project's main homepage.
    url='https://github.com/LG-1/EntityRelation',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',

    # Author details
    author='LG',
    author_email='ourantech@163.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
    ],

    # What does your project relate to?
    keywords='nlp EntityRelation entity relation dsnf',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['pyltp', 'jieba', 'tqdm', 'requests'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest', 'sphinx', 'sphinx_rtd_theme'],
        'test': ['coverage', 'nose'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={'EntityRelation': ['resource/user_dict.txt']},

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
    },
    test_suite="setup.EntityRelation_test_suite"
)
