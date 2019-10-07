#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
~$ whomst .
~$ whomst <path>
~$ whomst . > requirements.txt && pip install -r requirements.txt
"""
def main(path="."):
    # ENTRYPOINT
    import os
    cursor = set()
    result = set()
    answer = []
    exclude = set([
        "__pycache__",
        "lib",
        "env",
        "ENV",
        "venv",
        "VENV",
        "site-packages",
        "*.egg-info",
    ])

    # GATHER LIST OF ALL RELEVANT FILES
    for root, dirs, files in os.walk(path):
        if any(excl in root for excl in exclude):
            continue
        files[:] = [f for f in files if f.endswith(".py")]
        for fname in files:
            # EXTRACT IMPORT STATEMENT LINES
            with open(os.path.join(root, fname)) as f:
                file_data = f.read()
                for line in file_data.splitlines():
                    if "import" in line and line.startswith(("import", "from")):
                        cursor.add(line)

    # EXTRACT PACKAGE NAMES FROM IMPORT STATEMENTS
    for line in cursor:
        if line.startswith("import"):
            ln = line.strip("import").split(",")
            ln = list(map(str.strip, ln))
            for l in ln:
                if " as " in l:
                    l = l.split(" as ")[0].strip()
                    result.add(l)
                else:
                    result.add(l)
        elif line.startswith("from"):
            ln = between(line, "from", "import").split(".")[0].strip()
            result.add(ln)

    # OMIT BUILTIN LIBRARY MODULES
    builtins = built_in_modules("dict")
    for package in result:
        if package in builtins:
            pass
        else:
            answer.append(package)

    # PRINT TO CONSOLE
    terminal_output(*answer)

    # CREATE REQUIREMENTS FILE
    # touch_file(answer)

    # ----------------------- EOF -----------------------


# select string between 2 substrings
def between(s, start, end):
    return (s.split(start))[1].split(end)[0]


# prints to the console, now in technicolor!
def terminal_output(*args):
    import sys
    for arg in args:
        print("%s" % arg)


# create new dependencies file
def touch_file(packages, fname="requirements.txt"):
    """
    param: packages:     collection of type <str>
    creates new file in current directory
    """
    cwd = os.getcwd()
    with open(os.path.join(cwd, fname), "w") as f:
        for item in packages:
            f.write("%s\n" % item)


# list of included modules within Python 3.7
def built_in_modules(return_type="list"):
    built_in_modules = {
        "__future__":"",
        "__main__":"",
        "_dummy_thread":"",
        "_thread":"",
        "abc":"",
        "aifc":"",
        "argparse":"",
        "array":"",
        "ast":"",
        "asynchat":"",
        "asyncio":"",
        "asyncore":"",
        "atexit":"",
        "audioop":"",
        "base64":"",
        "bdb":"",
        "binascii":"",
        "binhex":"",
        "bisect":"",
        "builtins":"",
        "bz2":"",
        "calendar":"",
        "cgi":"",
        "cgitb":"",
        "chunk":"",
        "cmath":"",
        "cmd":"",
        "code":"",
        "codecs":"",
        "codeop":"",
        "collections":"",
        "colorsys":"",
        "compileall":"",
        "concurrent":"",
        "configparser":"",
        "contextlib":"",
        "contextvars":"",
        "copy":"",
        "copyreg":"",
        "cProfile":"",
        "crypt":"",
        "csv":"",
        "ctypes":"",
        "curses":"",
        "dataclasses":"",
        "datetime":"",
        "dbm":"",
        "decimal":"",
        "difflib":"",
        "dis":"",
        "distutils":"",
        "doctest":"",
        "dummy_threading":"",
        "email":"",
        "encodings":"",
        "ensurepip":"",
        "enum":"",
        "errno":"",
        "faulthandler":"",
        "fcntl":"",
        "filecmp":"",
        "fileinput":"",
        "fnmatch":"",
        "formatter":"",
        "fractions":"",
        "ftplib":"",
        "functools":"",
        "gc":"",
        "getopt":"",
        "getpass":"",
        "gettext":"",
        "glob":"",
        "grp":"",
        "gzip":"",
        "hashlib":"",
        "heapq":"",
        "hmac":"",
        "html":"",
        "http":"",
        "imaplib":"",
        "imghdr":"",
        "imp":"",
        "importlib":"",
        "inspect":"",
        "io":"",
        "ipaddress":"",
        "itertools":"",
        "json":"",
        "keyword":"",
        "lib2to3":"",
        "linecache":"",
        "locale":"",
        "logging":"",
        "lzma":"",
        "macpath":"",
        "mailbox":"",
        "mailcap":"",
        "marshal":"",
        "math":"",
        "mimetypes":"",
        "mmap":"",
        "modulefinder":"",
        "msilib":"",
        "msvcrt":"",
        "multiprocessing":"",
        "netrc":"",
        "nis":"",
        "nntplib":"",
        "numbers":"",
        "operator":"",
        "optparse":"",
        "os":"",
        "ossaudiodev":"",
        "parser":"",
        "pathlib":"",
        "pdb":"",
        "pickle":"",
        "pickletools":"",
        "pipes":"",
        "pkgutil":"",
        "platform":"",
        "plistlib":"",
        "poplib":"",
        "posix":"",
        "pprint":"",
        "profile":"",
        "pstats":"",
        "pty":"",
        "pwd":"",
        "py_compile":"",
        "pyclbr":"",
        "pydoc":"",
        "queue":"",
        "quopri":"",
        "random":"",
        "re":"",
        "readline":"",
        "reprlib":"",
        "resource":"",
        "rlcompleter":"",
        "runpy":"",
        "sched":"",
        "secrets":"",
        "select":"",
        "selectors":"",
        "shelve":"",
        "shlex":"",
        "shutil":"",
        "signal":"",
        "site":"",
        "smtpd":"",
        "smtplib":"",
        "sndhdr":"",
        "socket":"",
        "socketserver":"",
        "spwd":"",
        "sqlite3":"",
        "ssl":"",
        "stat":"",
        "statistics":"",
        "string":"",
        "stringprep":"",
        "struct":"",
        "subprocess":"",
        "sunau":"",
        "symbol":"",
        "symtable":"",
        "sys":"",
        "sysconfig":"",
        "syslog":"",
        "tabnanny":"",
        "tarfile":"",
        "telnetlib":"",
        "tempfile":"",
        "termios":"",
        "test":"",
        "textwrap":"",
        "threading":"",
        "time":"",
        "timeit":"",
        "tkinter":"",
        "token":"",
        "tokenize":"",
        "trace":"",
        "traceback":"",
        "tracemalloc":"",
        "tty":"",
        "turtle":"",
        "turtledemo":"",
        "types":"",
        "typing":"",
        "unicodedata":"",
        "unittest":"",
        "urllib":"",
        "uu":"",
        "uuid":"",
        "venv":"",
        "warnings":"",
        "wave":"",
        "weakref":"",
        "webbrowser":"",
        "winreg":"",
        "winsound":"",
        "wsgiref":"",
        "xdrlib":"",
        "xml":"",
        "xmlrpc":"",
        "zipapp":"",
        "zipfile":"",
        "zipimport":"",
        "zlib":"",
    }

    if return_type == "list":
        return built_in_modules
    elif return_type == "dict":
        return dict.fromkeys(built_in_modules)
    elif return_type == "set":
        return set(built_in_modules)


# ----------------------- -----------------------
if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', default=os.getcwd())
    args = parser.parse_args()

    main(path=args.path)
