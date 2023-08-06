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
    'version': '2.0.2',
    'description': 'Lists out permutations of lines in files.',
    'long_description': '# mixemup\n\n[![Build Status](https://travis-ci.com/tonikarppi/mixemup.svg?branch=master)](https://travis-ci.com/tonikarppi/mixemup)\n\n### A string combiner\n\nThis program takes as input a file of strings, and produces a list of combinations of these strings as output.\n\n## Installation\n\nRequires Python 3.7 or greater.\n\n```\npip install mixemup\n```\n\n## Usage\n\n```\nUsage: mixemup.py [OPTIONS] FILE_PATH\n\n  This program takes in a file with strings, and produces delimiter-\n  separated combinations of these strings.\n\nOptions:\n  -d, --delimiter TEXT     Set the delimiter.\n  -r, --prefix TEXT        Add the given string to the beginning of each line.\n  -o, --postfix TEXT       Add the given string to the end of each line.\n  -n, --min-parts INTEGER  Set the minimum number of parts in output. This\n                           count does not include prefixes and postfixes.\n  -m, --max-parts INTEGER  Set the maximum number of parts in output. This\n                           count does not include prefixes and postfixes.\n  --version                Show the version and exit.\n  --help                   Show this message and exit.\n\n```\n\n### Example\n\n```\n$ cat names.txt\nbob\nalice\njohn\njack\nsally\n```\n\n```\n$ mixemup names.txt\n\nbob\nalice\njohn\njack\nsally\nbob alice\nbob john\nbob jack\nbob sally\nalice john\nalice jack\nalice sally\njohn jack\njohn sally\njack sally\nbob alice john\nbob alice jack\nbob alice sally\nbob john jack\nbob john sally\nbob jack sally\nalice john jack\nalice john sally\nalice jack sally\njohn jack sally\nbob alice john jack\nbob alice john sally\nbob alice jack sally\nbob john jack sally\nalice john jack sally\nbob alice john jack sally\n```\n',
    'author': 'Toni Karppi',
    'author_email': 'karppitoni@gmail.com',
    'url': 'https://github.com/tonikarppi/mixemup',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
