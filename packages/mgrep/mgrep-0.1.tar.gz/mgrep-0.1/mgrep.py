from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import re
import sys

import click


STARTC = '\033[91m'
ENDC = '\033[0m'


class PathlibPath(click.Path):
    """A Click path type that returns a pathlib Path, not a string"""
    def convert(self, value, param, ctx):
        return Path(super().convert(value, param, ctx))


def collect_files(paths, recursive):
    files = []
    if not recursive:
        for path in paths:
            if path.is_file():
                files.append(path)
            elif path.is_dir():
                sys.stderr.write(f'grep: {path}: Is a directory')
        return files
    for path in paths:
        for subpath in path.rglob('*'):
            if subpath.is_file():
                files.append(subpath)
            elif subpath.is_dir():
                sys.stderr.write(f'grep: {subpath}: Is a directory')
    return files


def make_search_pattern(pattern, ignore_case):
    pattern = f'({pattern})'
    if ignore_case:
        return re.compile(pattern, re.IGNORECASE)
    return re.compile(pattern)


def grep_file(file, re_pattern):
    lines = []
    try:
        with open(file) as grepfile:
            for line in grepfile:
                if re_pattern.search(line)  is not None:
                    lines.append(line)
    except (IsADirectoryError, FileNotFoundError, UnicodeDecodeError):
        pass
    return lines


def print_result(result, re_pattern, color, print_filename):
    file, future = result
    prefix = f'{file}:' if print_filename else ''
    use_color = color.lower() == "always" or (color.lower() == "auto" and sys.stdout.isatty())
    if use_color:
        for line in future.result():
            line = re_pattern.sub(f'{STARTC}\\1{ENDC}', line)
            sys.stdout.write(f'{prefix}{line}')
    else:
        for line in future.result():
            sys.stdout.write(f'{prefix}{line}')


@click.command()
@click.option('-r', '--recursive', is_flag=True, default=False)
@click.option('-i', '--ignore-case', is_flag=True, default=False)
@click.option('-c', '--color', type=click.Choice(['always', 'never', 'auto']), default="auto")
@click.argument('pattern')
@click.argument('paths', nargs=-1, type=PathlibPath())
def cli(recursive, ignore_case, color, pattern, paths):
    files = collect_files(paths, recursive)
    print_filename = True if len(files) > 1 else False
    re_pattern = make_search_pattern(pattern, ignore_case)
    executor = ProcessPoolExecutor()
    results = []
    for file in files:
        future = executor.submit(grep_file, file, re_pattern)
        results.append((file, future))
    for result in results:
        print_result(result, re_pattern, color, print_filename)


if __name__ == '__main__':
    cli()
