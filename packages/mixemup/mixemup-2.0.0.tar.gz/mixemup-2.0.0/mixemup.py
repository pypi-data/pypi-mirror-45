import itertools
from typing import Generator, Iterable

import click
import pkg_resources

__version__ = pkg_resources.get_distribution("mixemup").version


def combine_strings(
    strings: Iterable[str],
    delimiter: str = " ",
    min_parts: int = 0,
    max_parts: int = None,
) -> Generator[str, None, None]:
    """
    Returns a generator for delimiter-separated combinations of the strings from
    `strings`. The combination sizes range from `min_parts` to the smaller of
    `max_parts` (if it is not `None`) and the number of items in `strings`.
    """
    strings_list = list(strings)
    iterations = len(strings_list) + 1
    if max_parts is not None:
        iterations = min(iterations, max_parts + 1)

    for i in range(min_parts, iterations):
        string_combinations = itertools.combinations(strings_list, i)
        for combination in string_combinations:
            yield delimiter.join(combination)


def read_lines(file_path: str) -> Generator[str, None, None]:
    """
    Returns a generator for the lines in a file. All trailing spaces and newlines are
    removed from each read line. The parameter `file_path` is the path to a text file
    for which the lines are to be fetched from.
    """
    with open(file_path) as f:
        for line in f:
            yield line.rstrip()


def print_combination(
    combination: str, delimiter: str = " ", prefix: str = None, postfix: str = None
) -> None:
    """
    Prints the `combination` string on its own line. This string is delimited by
    `delimiter`, preceded by the `prefix` string, and followed by the `postfix` string.
    """
    if prefix is not None:
        print(prefix, end=delimiter)

    print(combination, end="")

    if postfix is not None:
        print(delimiter if len(combination) > 0 else "", end=postfix)
    print()


def main(
    file_path: str,
    delimiter: str = " ",
    prefix: str = None,
    postfix: str = None,
    min_parts: int = 0,
    max_parts: int = None,
) -> None:
    """
    Runs the program. The parameter `file_path` is the path to the file which is to be
    read. The `delimiter` argument specifies which delimiter to use to separate the
    output strings. The parameters `prefix` and `postfix` are optional strings appended
    and prepended to the output lines. The `min_parts` parameter specifies the minimum
    number of parts in an output line. The `max_parts` parameter specifies the maximum
    number of parts in an output line (a value of `None` specifies no maximum).

    The function raises a `FileNotFoundError` if it tries to read a file which does
    not exist.
    """
    lines = read_lines(file_path)
    lines_with_text = (line for line in lines if len(line) > 0)
    line_combinations = combine_strings(
        lines_with_text, delimiter=delimiter, min_parts=min_parts, max_parts=max_parts
    )
    for combination in line_combinations:
        print_combination(
            combination, delimiter=delimiter, prefix=prefix, postfix=postfix
        )


@click.command()
@click.argument("file_path")
@click.option("-d", "--delimiter", default=" ", help="Set the delimiter.")
@click.option(
    "-r",
    "--prefix",
    default=None,
    help="Add the given string to the beginning of each line.",
)
@click.option(
    "-o",
    "--postfix",
    default=None,
    help="Add the given string to the end of each line.",
)
@click.option(
    "-n",
    "--min-parts",
    default=0,
    help="Set the minimum number of parts in output. This count does not include "
    "prefixes and postfixes.",
    type=click.INT,
)
@click.option(
    "-m",
    "--max-parts",
    default=None,
    help="Set the maximum number of parts in output. This count does not include "
    "prefixes and postfixes.",
    type=click.INT,
)
@click.version_option(__version__)
def console_start(
    file_path: str,
    delimiter: str,
    prefix: str,
    postfix: str,
    min_parts: int,
    max_parts: int,
) -> None:
    """
    This program takes in a file with strings, and produces delimiter-separated
    combinations of these strings.
    """
    import sys

    error_message = None
    try:
        main(
            file_path,
            delimiter=delimiter,
            prefix=prefix,
            postfix=postfix,
            min_parts=min_parts,
            max_parts=max_parts,
        )
    except FileNotFoundError:
        error_message = f"The file '{file_path}' could not be found."

    if error_message is not None:
        print(f"Error: {error_message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    console_start()
