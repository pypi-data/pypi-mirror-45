# mixemup

### Combine and mix strings

This program takes in a file of strings, and produces combinations of different lengths of these strings. This is pretty useful for when you want to test parameter input for programs.

## Installation
Requires Python 3.7 or greater.
```
pip install mixemup
```

## Usage

```
Usage: mixemup [OPTIONS] FILE_PATH

  This program takes in a file with strings, and produces space-
  separated combinations of these strings.

Options:
  --prefix TEXT       Add the given string to the beginning of each line.
  --postfix TEXT      Add the given string to the end of each line.
  --max-args INTEGER  Set the max number of arguments in output. This
                      count does not include prefixes and postfixes.
  --version           Show the version and exit.
  --help              Show this message and exit.
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