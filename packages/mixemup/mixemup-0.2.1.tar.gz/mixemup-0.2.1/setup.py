# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['mixemup']
install_requires = \
['click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['mixemup = mixemup:console_start']}

setup_kwargs = {
    'name': 'mixemup',
    'version': '0.2.1',
    'description': 'Lists out permutations of lines in files.',
    'long_description': None,
    'author': 'Toni Karppi',
    'author_email': 'karppitoni@gmail.com',
    'url': 'https://github.com/tonikarppi/mixemup',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
