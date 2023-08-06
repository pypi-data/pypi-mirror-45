"""pimple: Summarize your unit tests"""

import importlib.util
from pathlib import Path
import sys
import textwrap

import click


def import_module(path):
    """Import a module from a filepath.

    Args:
        path (PathLike): The file to import.

    Returns:
        module: The imported module.
    """
    # Add the pwd to the python path.
    pwd = str(Path.cwd())
    if pwd not in sys.path:
        sys.path.append(pwd)
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def underline(text: str, char: str = "=") -> str:
    """Underline the given text.

    Args:
        text (str):
            The text to be underlined.
        char (str, optional):
            The character with which to underline the text. (default: `=`)
    """
    return str(text) + "\n" + char * len(str(text))


def flush_left(text: str) -> str:
    """Remove leading whitespace from each line."""
    if text:
        first_line, sep, end_lines = text.partition("\n")
        return first_line + sep + textwrap.dedent(end_lines)
    return ""


@click.command()
@click.argument("directory", type=click.Path(exists=True, file_okay=False))
@click.argument("output_file", type=click.File("w"), default="testcase_summary.rst")
def main(directory, output_file):
    """Find test files in the given DIRECTORY and compile a summary of the test modules,
    classes, and functions from their docstrings.
    The result is saved to OUTPUT_FILE (default: testcase_summary.rst).
    """
    output_lines = [underline("Test cases")]

    test_dir = Path(directory)
    test_files = test_dir.glob("**/test_*.py")
    for test_file in test_files:
        module = import_module(test_file)
        output_lines.append(underline(test_file, "-"))
        output_lines.append(flush_left(module.__doc__).rstrip())

        funcs = [attr for attr in dir(module) if attr.startswith("test_")]
        classes = [attr for attr in dir(module) if attr.startswith("Test")]

        for func_name in funcs:
            func = getattr(module, func_name)
            output_lines.append(underline(func.__name__, "^"))
            output_lines.append(flush_left(func.__doc__).rstrip())

        for class_name in classes:
            cls = getattr(module, class_name)
            output_lines.append(underline(cls.__name__, "^"))
            output_lines.append(flush_left(cls.__doc__).rstrip())

            funcs = [attr for attr in dir(cls) if attr.startswith("test_")]
            for func_name in funcs:
                func = getattr(cls, func_name)
                output_lines.append(underline(func.__name__, "'"))
                output_lines.append(flush_left(func.__doc__).rstrip())

    output = "\n\n".join(output_lines)
    output_file.write(output)
