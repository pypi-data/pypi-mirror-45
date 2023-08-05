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