# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['rtd_poetry']
setup_kwargs = {
    'name': 'rtd-poetry',
    'version': '0.1.0',
    'description': 'Execute poetry install with dev dependencies on RTD',
    'long_description': None,
    'author': 'Chris Hunt',
    'author_email': 'chrahunt@gmail.com',
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
