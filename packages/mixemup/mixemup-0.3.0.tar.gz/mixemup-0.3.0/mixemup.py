import itertools
import click
import pkg_resources

__version__ = pkg_resources.get_distribution("mixemup").version


def combine_strings(strings, max_args=None):
    """
    Returns a generator for space-separated combinations of the strings from the input.
    The parameter `strings` is an iterable/generator of strings.
    The combinations range from length 0 to the number of items in `strings`.
    """
    strings_list = list(strings)
    iterations = len(strings_list) + 1
    if max_args is not None:
        iterations = min(iterations, max_args + 1)

    for i in range(iterations):
        string_combinations = itertools.combinations(strings_list, i)
        for combination in string_combinations:
            yield " ".join(combination)


def read_lines(file_path):
    """
    Returns a generator for the lines in a file. The parameter `file_path` is the path
    to a text file for which the lines are to be fetched from.
    """
    with open(file_path) as f:
        for line in f:
            yield line.strip()


def main(file_path, prefix="", postfix="", max_args=None):
    """
    Runs the program. The parameter `file_path` is the path to the file which is to be
    read. The parameters `prefix` and `postfix` are optional strings appended and
    prepended to the output lines. The function raises a `FileNotFoundError` if it
    tries to read a file which does not exist.
    """

    lines = read_lines(file_path)
    lines_with_text = (line for line in lines if len(line) > 0)
    line_combinations = combine_strings(lines_with_text, max_args)
    for combination in line_combinations:
        print(prefix, end=" ")
        if len(combination) != 0:
            print(combination, end=" ")
        print(postfix)


@click.command()
@click.argument("file_path")
@click.option(
    "--prefix", default="", help="Add the given string to the beginning of each line."
)
@click.option(
    "--postfix", default="", help="Add the given string to the end of each line."
)
@click.option(
    "--max-args",
    default=None,
    help="Set the max number of arguments in output. This count does not include "
    "prefixes and postfixes.",
    type=click.INT,
)
@click.version_option(__version__)
def console_start(file_path, prefix, postfix, max_args):
    """
    This program takes in a file with strings, and produces space-separated
    combinations of these strings.
    """
    import sys

    error_message = None
    try:
        main(file_path, prefix, postfix, max_args)
    except FileNotFoundError:
        error_message = f"The file '{file_path}' could not be found."

    if error_message is not None:
        print(f"Error: {error_message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    console_start()
