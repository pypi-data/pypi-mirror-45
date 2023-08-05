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
    'version': '0.2.4',
    'description': 'Lists out permutations of lines in files.',
    'long_description': '# mixemup\n\n### Combine and mix strings\n\nThis program takes in a file of strings, and produces combinations of different lengths of these strings. This is pretty useful for when you want to test parameter input for programs.\n\n## Installation\nRequires Python 3.7 or greater.\n```\npip install mixemup\n```\n\n## Usage\n\n\n```\n$ cat names.txt \n\nbob\nalice\njohn\njack\nsally\n```\n\n```\n$ mixemup names.txt\n\n\nbob \nalice \njohn \njack \nsally \nbob alice \nbob john \nbob jack \nbob sally \nalice john \nalice jack \nalice sally \njohn jack \njohn sally \njack sally \nbob alice john \nbob alice jack \nbob alice sally \nbob john jack \nbob john sally \nbob jack sally \nalice john jack \nalice john sally \nalice jack sally \njohn jack sally \nbob alice john jack \nbob alice john sally \nbob alice jack sally \nbob john jack sally \nalice john jack sally \nbob alice john jack sally\n```',
    'author': 'Toni Karppi',
    'author_email': 'karppitoni@gmail.com',
    'url': 'https://github.com/tonikarppi/mixemup',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
