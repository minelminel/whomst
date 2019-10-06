#!/usr/bin/env python
import os

def get_calling_path():
    pth = os.getcwd()
    print(pth)



def all_lines_with_imports(pth, prints=True):
    '''
    returns a list of all import statements in the current path.
    common package directories are omitted.
    '''
    pth = os.path.abspath(pth)
    cwd = os.getcwd()
    cursor = []
    count_lines = 0
    count_files = 0
    exclude = set(['__pycache__', 'env', 'ENV', 'venv', 'VENV', 'site-packages', '*.egg-info'])
    for root, dirs, files in os.walk(pth, topdown=True):
        if 'site-packages' in root:
            continue
        dirs[:] = [d for d in dirs if d not in exclude]
        files[:] = [f for f in files if f.endswith('.py')]
        dirpath = os.path.dirname(os.path.abspath(dirs.pop()))
        print(dirpath)
        for filename in files:
            print(filename)
            file = open(os.path.join(dirpath, filename), 'r')
            file_data = file.read()
            count_files += 1
            # extract import statements
            for line in file_data.splitlines():
                if line.startswith(('import', 'from')):
                    cursor.append(line)
                count_lines += 1
    if prints:
        from pprint import pprint
        pprint(cursor)
        print('Path: {0}'.format(cwd))
        print('Files: {0}'.format(count_files))
        print('Lines: {0}'.format(count_lines))

    return cursor


def between(s, start, end):
    return (s.split(start))[1].split(end)[0]


def interpret_results(lines):
    '''
    filter and clean the list of import statements.
    try to break complex lines into their atomic parts,
        if any are unsure, omit.
    '''
    cursor = set()
    for line in lines:
        # import foo
        # import foo, bar
        if line.startswith('import') and 'as' not in line:
            ln = line.replace('import', '').split(',')
            ln = list(map(str.strip, ln))
            cursor.update(ln)
        # from foo import f
        # from foo import f as func
        if line.startswith('from') and 'import' in line:
            ln = between(line, 'from', 'import').strip()
            cursor.add(ln)

    return cursor


def touch_file(packages, fname='requirements.txt'):
    '''
    param: results:     a set of strings
    creates new file in current directory
    '''
    cwd = os.getcwd()
    with open(os.path.join(cwd, fname), 'w') as f:
        for item in packages:
            f.write("%s\n" % item)


def console_output(packages):
    for item in packages:
        print(item)


# lines = all_lines_with_imports(prints=False)
# results = interpret_results(lines)
# console_output(results)
# touch_file(results)



'''
// modes of operation

1. display all import statements
2. import statements with path displayed
3. print packages
    3.1 omit site-packages and relative imports
4. create requirements.txt file
5. promiscuous install


'''
