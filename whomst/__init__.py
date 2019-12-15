#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
usage: whomst [-h] [-s SKIP [SKIP ...]] [-e] [-v] path

Easily preview package dependencies for Python repositories

positional arguments:
  path                  Path of top-level directory, use `.` for cwd

optional arguments:
  -h, --help            show this help message and exit
  -s SKIP [SKIP ...], --skip SKIP [SKIP ...]
  -e, --exhaustive      Bypass omitted directories (VENV, etc.) and show all
                        discovered imports
  -v, --verbose         Print operational info (useful for debugging)

$ whomst {path} > requirements.txt
"""
import os, sys, argparse

def walk_files(path, exclude, verbose=False):
    """
    Generator which yields an absolute path to all Python files
    under the provided path, skipping any files that contain in
    its path a directory that is present in `exclude`.

    @param: path        path to top-level directory to recursively search
    @param: exclude     <set 'str'> names of directories to omit if in path
    """

    # If supplied path resolves to a single file, return a singular reference.
    # This allows the same procedure to be used within the main procedure,
    # with the loop only running one time.
    if os.path.isfile(path):
        yield path

    # Otherwise, we can assume the supplied path is a reference to a directory,
    # in which case we will have to recursively explore the contained files.
    for root, dirs, files in os.walk(path):

        # Bypass any paths containing one of the specified exlusion directories
        if any(excl in root for excl in exclude):
            continue

        # Only concerned with `.py` files, important to note that executable files
        # with a valid Python #!/ she-bang will NOT be caught by this procedure.
        # This is a sufficiently nuanced edge case for us to not concern ourselves with.
        files[:] = [f for f in files if f.endswith(".py")]
        for file in files:
            yield os.path.join(root, file)
    # --[EOF]--


def make_exclusions(skip=[], exhaustive=False, verbose=False, **kwargs):
    """
    Assemble the set of folders we should check for
    in the .py file path and if found ignore that file.
    Useful for omitting VENV libraries which may be
    in a local folder, plus pycache files.

    @param: skip           <list> directory names to skip
    @param: exhaustive     <bool> override all exclusions
    """
    exclude = set()

    # If the user has supplied additional elements, include them
    if skip:
        exclude = exclude.union(skip)

    # If `exhaustive` is True, do not omit ANY directories. This is useful
    # in cases where a Python repo might be part of a larger, multi-language repo.
    if not exhaustive:
        # Include a base set of common directories to ignore, both to
        # speed-up the search by skipping irrelevant paths, as well as
        # to avoid searching virtual environment assets.
        commons = ["__pycache__","lib","bin","site-packages",
                "env","ENV","venv","VENV",".egg-info",".git"]
        exclude = exclude.union(commons)

    # Display the collection of directories we are skipping, to aid with debugging.
    if verbose:
        info("skip", exclude or {})

    return exclude
    # --[EOF]--


def read_imports(full_name):
    """
    Reads the file line-by-line and captures ALL lines
    containing a valid import statement. Lines are kept
    as unified strings for further post-processing.
    Commented lines are ignored.

    @param: full_name       <str> abspath to python file
    """
    # TODO: do this with RegEx capture groups
    # TODO: IF LINE HAS `()` CAPTURE UNTIL IT CLOSES

    cursor = set()

    # Read the contents of the file and return a list of all lines
    with open(full_name) as f:
        lines = f.read().splitlines()

    # Core of the operation right here. Check all elements in the
    # lines of lines and capture all lines containing an import statement.
    for line in lines:
        if line.startswith("#"):
            continue

        # Ensure that line starts with a valid statement, this is
        # useful for ignoring invalid matches like when the word `import`
        # appears in a function name, or when there is a variable called
        # `_import` or something similar.
        elif "import" in line and line.startswith(("import", "from")):
            cursor.add(line)

    return cursor
    # --[EOF]--


def between(s, start, end):
    """
    Extracts contents between 2 bookend strings, non-inclusive.

    >>> s = 'from numpy import my_array, my_matrix'
    >>> start,end = 'from','import'
    >>> between(s,start,end)
    'numpy'

    @param: s         <str> the string to be extracted from
    @param: start     <str> opening capture
    @param: end       <str> closing capture
    """
    return (s.split(start))[1].split(end)[0].strip()


def clean_lines(cursor):
    """
    Takes in a set of strings, where each string is a file line
    containing some form of an import statement. We want to
    extract the cannonical name of the package, ignoring any
    relative imports and aliases.

    @param: cursor      <set> strings of import statements
    """
    result = set()

    # Extract only the top-level package names from import statements
    for line in cursor:

        # Case 1:: `import PKG ...`
        if line.startswith("import"):
            # Remove `import` from line, split into separate packages
            ln = line.replace("import", "").split(",")
            # Remove leading+trailing whitespace so that condition
            # checks like .startswith() will behave as desired.
            ln = list(map(str.strip, ln))
            # focus on each statement from the single line
            for l in ln:

                # Case 1a:: `import PGK as some_alias ...`
                if " as " in l:
                    l = l.split(" as ")[0].strip()
                    l = l.split(".")[0]
                    result.add(l)

                # Case 1b:: `import .PKG as relative_alias`
                # we can disregard relative imports since they
                # can safely be assumed to be from the same package
                elif l.startswith("."):
                    continue

                # Case 1c:: `import torch.nn.Functional as F`
                # we want to isolate the top-level package
                elif "." in l:
                    l = l.split(".")[0]
                    result.add(l)

                # If all previous conditionals fail, the statement
                # can be considered a vanilla import and is safe as-is
                else:
                    result.add(l)

        # Case 2:: `from PKG import ...`
        elif line.startswith("from"):
            # `import numpy as np` --> `np`
            ln = between(line, "from", "import")
            # ignore relative imports
            if not ln.startswith("."):
                ln = ln.split(".")[0].strip()
                result.add(ln)

    # Omit any empty strings that may have slipped through
    no_empties = filter(bool, result)
    return sorted(no_empties)
    # --[EOF]--


def ignore_included(cursor, builtins, all_imports=False):
    """
    Cross-reference the import list with the Python standard library.
    Allow for bypassing such that ALL non-relative imports are included.

    @param: cursor          <set> strings, captured import statements
    @param: builtins        <set> strings, standard library packages
    @param: all_imports     <bool> include standard library imports
    """
    # If specified, return ALL imports, include those from standard library
    if all_imports:
        return sorted(list(cursor))

    result = []
    # Disregard some basic, vague elements that might have slipped through
    commons = set(["bin","lib","include","share","tests"])

    # Ensure that all captured packages are outside the standard library
    for pkg in cursor:
        if (pkg not in commons):
            if (pkg not in builtins):
                result.append(pkg)

    # Alphabetize the list as a convenience for the user
    return sorted(result)
    # --[EOF]--


def terminal(*args):
    for _,arg in enumerate(args):
        print("{}".format(arg))


def info(label, *msg):
    if len(msg) < 2:
        print("==> [{}] {}".format(label, *msg))
    else:
        print("==> [{}]".format(label))
        for m in msg:
            print(m)


def cli(args=sys.argv[1:]):
    """
    Command-line interface, entrypoint for package.
    """

    ap = argparse.ArgumentParser(
        prog='whomst',
        description='Easily preview package dependencies for Python repositories',
        epilog="$ whomst {path} > requirements.txt"
    )
    ap.add_argument(
        'path',
        help='Path of top-level directory, use `.` for cwd',
    )
    ap.add_argument(
        '-s',
        '--skip',
        nargs='+',
        default=[],
        help="",
    )
    ap.add_argument(
        '-e',
        '--exhaustive',
        default=False,
        action="store_true",
        help="Bypass omitted directories (VENV, etc.) and show all discovered imports",
    )
    ap.add_argument(
        '-a',
        '--all-imports',
        default=False,
        action="store_true",
        help="Include standard library package imports in result",
    )
    ap.add_argument(
        '-v',
        '--verbose',
        default=False,
        action="store_true",
        help="Print operational info (useful for debugging)",
    )

    return ap.parse_args(args)
    # --[EOF]--


def preflight(args):
    """
    Perform checks on supplied arguments, consolidate path, etc.

    @param: args    <Namespace> argparse parsed result
    """
    # Treat paths as relative to the calling directory
    here = os.getcwd()
    if args.verbose: info("here", here)

    # Valid path to directory. Reduce the path, replacing relative refs
    if os.path.isdir(args.path):
        args.path = os.path.normpath(os.path.join(here, args.path))
        if args.verbose: info("args", args.__dict__)
    # Valid path to a file. Reduce the path, replacing relative refs
    elif os.path.isfile(args.path):
        args.path = os.path.normpath(os.path.join(here, args.path))
        if args.verbose: info("args", args.__dict__)
    else:
        # Fail if the supplied path does not exist, or if formatted incorrectly
        print("* ERROR - InvalidPath {}".format(args.path))
        sys.exit(1)

    return args
    # --[EOF]--


def main():
    args = preflight(cli())
    exclude = make_exclusions(args.skip, args.exhaustive, args.verbose)
    cursor = set()
    for abspath in walk_files(args.path, exclude, verbose=args.verbose):
        lines = read_imports(abspath)
        cursor = cursor.union(lines)
    cursor = clean_lines(cursor)
    final = ignore_included(cursor, builtins, args.all_imports)
    terminal(*final)
    sys.exit(0)
    # --[EOF]--


builtins = set([
  "__future__",
  "__main__",
  "_dummy_thread",
  "_thread",
  "abc",
  "aifc",
  "argparse",
  "array",
  "ast",
  "asynchat",
  "asyncio",
  "asyncore",
  "atexit",
  "audioop",
  "base64",
  "bdb",
  "binascii",
  "binhex",
  "bisect",
  "builtins",
  "bz2",
  "calendar",
  "cgi",
  "cgitb",
  "chunk",
  "cmath",
  "cmd",
  "code",
  "codecs",
  "codeop",
  "collections",
  "colorsys",
  "compileall",
  "concurrent",
  "configparser",
  "contextlib",
  "contextvars",
  "copy",
  "copyreg",
  "cProfile",
  "crypt",
  "csv",
  "ctypes",
  "curses",
  "dataclasses",
  "datetime",
  "dbm",
  "decimal",
  "difflib",
  "dis",
  "distutils",
  "doctest",
  "dummy_threading",
  "email",
  "encodings",
  "ensurepip",
  "enum",
  "errno",
  "faulthandler",
  "fcntl",
  "filecmp",
  "fileinput",
  "fnmatch",
  "formatter",
  "fractions",
  "ftplib",
  "functools",
  "gc",
  "getopt",
  "getpass",
  "gettext",
  "glob",
  "grp",
  "gzip",
  "hashlib",
  "heapq",
  "hmac",
  "html",
  "http",
  "imaplib",
  "imghdr",
  "imp",
  "importlib",
  "inspect",
  "io",
  "ipaddress",
  "itertools",
  "json",
  "keyword",
  "lib2to3",
  "linecache",
  "locale",
  "logging",
  "lzma",
  "macpath",
  "mailbox",
  "mailcap",
  "marshal",
  "math",
  "mimetypes",
  "mmap",
  "modulefinder",
  "msilib",
  "msvcrt",
  "multiprocessing",
  "netrc",
  "nis",
  "nntplib",
  "numbers",
  "operator",
  "optparse",
  "os",
  "ossaudiodev",
  "parser",
  "pathlib",
  "pdb",
  "pickle",
  "pickletools",
  "pipes",
  "pkgutil",
  "platform",
  "plistlib",
  "poplib",
  "posix",
  "pprint",
  "profile",
  "pstats",
  "pty",
  "pwd",
  "py_compile",
  "pyclbr",
  "pydoc",
  "queue",
  "quopri",
  "random",
  "re",
  "readline",
  "reprlib",
  "resource",
  "rlcompleter",
  "runpy",
  "sched",
  "secrets",
  "select",
  "selectors",
  "shelve",
  "shlex",
  "shutil",
  "setuptools",
  "signal",
  "site",
  "smtpd",
  "smtplib",
  "sndhdr",
  "socket",
  "socketserver",
  "spwd",
  "sqlite3",
  "ssl",
  "stat",
  "statistics",
  "string",
  "stringprep",
  "struct",
  "subprocess",
  "sunau",
  "symbol",
  "symtable",
  "sys",
  "sysconfig",
  "syslog",
  "tabnanny",
  "tarfile",
  "telnetlib",
  "tempfile",
  "termios",
  "test",
  "textwrap",
  "threading",
  "time",
  "timeit",
  "tkinter",
  "token",
  "tokenize",
  "trace",
  "traceback",
  "tracemalloc",
  "tty",
  "turtle",
  "turtledemo",
  "types",
  "typing",
  "unicodedata",
  "unittest",
  "urllib",
  "uu",
  "uuid",
  "venv",
  "warnings",
  "wave",
  "weakref",
  "webbrowser",
  "winreg",
  "winsound",
  "wsgiref",
  "xdrlib",
  "xml",
  "xmlrpc",
  "zipapp",
  "zipfile",
  "zipimport",
  "zlib"
])


if __name__ == '__main__':
    main()
