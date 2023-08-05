# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os.path

readme = ''
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst'), 'r', 'utf-8') as stream:
    readme = stream.read()

setup(
    long_description=readme,
    name='dephell',
    version='0.4.1',
    description='Dependency resolution for Python',
    python_requires='>=3.5',
    project_urls={'repository': 'https://github.com/dephell/dephell'},
    author='Gram',
    author_email='master_fess@mail.ru',
    license='MIT',
    keywords='dephell packaging dependency dependencies venv licenses pip poetry pipfile pipenv setuptools',
    classifiers=[
        'Development Status :: 4 - Beta', 'Environment :: Console',
        'Framework :: Setuptools Plugin', 'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python', 'Topic :: Security',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points={'console_scripts': ['dephell = dephell.cli:entrypoint']},
    packages=[
        'dephell', 'dephell.actions', 'dephell.commands', 'dephell.config',
        'dephell.controllers', 'dephell.converters', 'dephell.models',
        'dephell.repositories', 'dephell.repositories.git'
    ],
    package_data={'dephell': ['templates/*.j2']},
    install_requires=[
        'aiohttp', 'appdirs', 'attrs', 'cerberus', 'dephell-archive',
        'dephell-discover', 'dephell-licenses', 'dephell-links',
        'dephell-markers', 'dephell-pythons', 'dephell-shells',
        'dephell-specifier', 'dephell-venvs', 'jinja2', 'm2r', 'packaging',
        'pip>=18.0', 'requests', 'tomlkit', 'yaspin'
    ],
    extras_require={
        'full': ['aiofiles', 'autopep8', 'colorama', 'graphviz', 'yapf'],
        'docs': [
            'pygments-github-lexers', 'recommonmark', 'sphinx',
            'sphinx-rtd-theme'
        ],
        'dev': [
            'pygments-github-lexers', 'pytest', 'recommonmark', 'sphinx',
            'sphinx-rtd-theme'
        ],
        'tests': ['pytest']
    },
)
