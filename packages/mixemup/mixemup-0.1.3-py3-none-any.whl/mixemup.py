import itertools
import click


def combine_strings(strings):
    """
    Returns a generator for space-separated combinations of the strings from the input.
    The parameter `strings` is an iterable/generator of strings.
    The combinations range from length 0 to the number of items in `strings`.
    """
    strings_list = list(strings)
    for i in range(len(strings_list) + 1):
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
            if len(line) > 0:
                yield line.strip()


def main(file_path, prefix, postfix):
    """
    Runs the program. Takes in a list of arguments, which is expected to consist of a
    file path to the lines to be mixed. The function returns a pair (success, message),
    that signifies whether the finished without errors, and a message to be shown
    to the user when exiting.
    """

    lines = read_lines(file_path)
    line_combinations = combine_strings(lines)
    for combination in line_combinations:
        print(prefix, end=" ")
        if len(combination) != 0:
            print(combination, end=" ")
        print(postfix)


@click.command()
@click.argument("file_path")
@click.option(
    "--prefix", default="", help="Adds the given string to the beginning of each line."
)
@click.option(
    "--postfix", default="", help="Adds the given string to the end of each line."
)
def console_start(file_path, prefix, postfix):
    """
    Runs the main program. This function handles taking input from the user, and
    handling erroneous input.
    """
    import sys

    error_message = None
    try:
        main(file_path, prefix, postfix)
    except FileNotFoundError:
        error_message = f"The file '{file_path}' could not be found."

    if error_message is not None:
        print(f"Error: {error_message}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    console_start()
