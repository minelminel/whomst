#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys
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
def walk_files(path, exclude, verbose=False):
    """
    Generator which yields an absolute path to all Python files
    under the provided path, skipping any files that contain in
    its path a directory that is present in `exclude`.

    @param: path        path to top-level directory to recursively search
    @param: exclude     <set 'str'> names of directories to omit if in path
    """
    if verbose: info("path", path)
    for root, dirs, files in os.walk(path):
        if any(excl in root for excl in exclude):
            continue
        files[:] = [f for f in files if f.endswith(".py")]
        for file in files:
            yield os.path.join(root, file)


def make_exclusions(skip=[], exhaustive=False, verbose=False, **kwargs):
    """
    Assemble the set of folders we should check for
    in the .py file path and if found ignore that file.
    Useful for omitting VENV libraries which may be
    in a local folder, plus pycache files.

    @param: skip           <list> directory names to skip
    @param: exhaustive     <bool> override all exclusions
    """
    if exhaustive:
        return set()
    exclude = set(
        ["__pycache__", ".git", "lib",
        "env", "ENV", "venv", "VENV",
        "site-packages", ".egg-info"]
    )
    if skip:
        exclude = exclude.union(skip)
    if verbose: info("skip", exclude)
    return exclude


def read_imports(full_name):
    """
    Reads the file line-by-line and captures ALL lines
    containing a valid import statement. Lines are kept
    as unified strings for further post-processing.
    Commented lines are ignored.

    @param: full_name       <str> abspath to python file
    """
    # TODO: IF LINE HAS `()` CAPTURE UNTIL IT CLOSES
    # TODO: do this with RegEx capture groups
    cursor = set()
    capture,cache = False,[]
    with open(full_name) as f:
        lines = f.read().splitlines()
    for line in lines:
        if line.startswith("#"):
            continue
        # elif capture:
        #     cache.append(line)
        #     if ")" in line:
        #         capture = False
        #         cursor.add(' '.join(cache))
        #         cache.clear()
        #
        # elif ( "(" in line ) and ( ")" not in line ):
        #     capture = True
        #     cache.append(line)
        elif "import" in line and line.startswith(("import", "from")):
            cursor.add(line)
    return cursor


def between(s, start, end):
    """
    Extracts contents between 2 bookend strings, non-inclusive.

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
    for line in cursor:
        if line.startswith("import"):
            ln = line.replace("import", "").split(",")
            ln = list(map(str.strip, ln))
            for l in ln:
                if " as " in l:
                    l = l.split(" as ")[0].strip()
                    l = l.split(".")[0]
                    result.add(l)
                elif "." in l:
                    l = l.split(".")[0]
                    result.add(l)
                else:
                    result.add(l)
        elif line.startswith("from"):
            ln = between(line, "from", "import")
            if not ln.startswith("."):
                ln = ln.split(".")[0].strip()
                result.add(ln)
    no_empties = filter(bool, result)
    return sorted(no_empties)


def ignore_included(cursor, builtins):
    """
    Cross-reference the import list with the Python standard library.
    """
    result = []
    commons = set(["bin","lib","include","share","tests"])
    for pkg in cursor:
        if (pkg not in builtins) and (pkg not in commons):
            result.append(pkg)
    return sorted(result)


def terminal(*args):
    for _,arg in enumerate(args):
        print("{}".format(arg))


def info(label, msg):
    print("==> [{}] {}".format(label, msg))


def cli():
    """
    # TODO: add support for omitting additional provided dir names
    # TODO: add support for not omitting any exclude dirs
    # TODO: add verbose mode that prints the search path, exclude dirs, files searched, raw statements found
    # TODO: add support for including standard library imports as well
    """
    import argparse
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
        '-v',
        '--verbose',
        default=False,
        action="store_true",
        help="Print operational info (useful for debugging)",
    )
    args = ap.parse_args()
    if os.path.exists(args.path) or os.path.isdir(args.path):
        return args
    raise FileNotFoundError("[InvalidPath] %s" % args.path)


def main():
    args = cli()
    exclude = make_exclusions(args.skip, args.exhaustive, args.verbose)
    cursor = set()
    for abspath in walk_files(args.path, exclude, verbose=args.verbose):
        lines = read_imports(abspath)
        cursor = cursor.union(lines)
    cursor = clean_lines(cursor)
    final = ignore_included(cursor, builtins)
    terminal(*final)
    sys.exit(0)


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
