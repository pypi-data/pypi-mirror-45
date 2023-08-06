# mixemup

[![Build Status](https://travis-ci.com/tonikarppi/mixemup.svg?branch=master)](https://travis-ci.com/tonikarppi/mixemup)

### A string combiner

This program takes as input a file of strings, and produces a list of combinations of these strings as output.

## Installation

Requires Python 3.7 or greater.

```
pip install mixemup
```

## Usage

```
Usage: mixemup.py [OPTIONS] FILE_PATH

  This program takes in a file with strings, and produces delimiter-
  separated combinations of these strings.

Options:
  -d, --delimiter TEXT     Set the delimiter.
  -r, --prefix TEXT        Add the given string to the beginning of each line.
  -o, --postfix TEXT       Add the given string to the end of each line.
  -n, --min-parts INTEGER  Set the minimum number of parts in output. This
                           count does not include prefixes and postfixes.
  -m, --max-parts INTEGER  Set the maximum number of parts in output. This
                           count does not include prefixes and postfixes.
  --version                Show the version and exit.
  --help                   Show this message and exit.

```

### Example

```
$ cat names.txt
bob
alice
john
jack
sally
```

```
$ mixemup names.txt

bob
alice
john
jack
sally
bob alice
bob john
bob jack
bob sally
alice john
alice jack
alice sally
john jack
john sally
jack sally
bob alice john
bob alice jack
bob alice sally
bob john jack
bob john sally
bob jack sally
alice john jack
alice john sally
alice jack sally
john jack sally
bob alice john jack
bob alice john sally
bob alice jack sally
bob john jack sally
alice john jack sally
bob alice john jack sally
```
