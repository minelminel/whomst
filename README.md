# whomst

# about
`whomst` is an easy way to preview dependencies within a Python directory structure. Whichever directory the script is called from within, a recursive tree will be walked while ignoring a specific set of directories that might clutter the output, namely common virtualenv directories as well as anything with `site-package` in its path. The script will print the results to the terminal, meaning you can easily pipe the output to a requirements.txt file if you so wish. Currently, it only works in Python3 but at some point I will port it over such that systems coming preinstalled with Python2 will be supported.

There are 2 ways to install and use the script- either install it as a PyPI package (or install from source) into a (fresh) virtualenv, or installing the binary directly to /usr/bin. The second method is recommended for regular use, while the first is great for test driving and quick, one-off usage.

---
# installation to /usr/bin
1. Clone the repository
```bash
git clone https://github.com/minelminel/whomst.git
cd whomst
```

2. Run the install script
```bash
chmod +x install
./install
```
l
3. Try it out!
```bash
#
```

# installation as Python package
1. Clone the repository
```bash
git clone https://github.com/minelminel/whomst.git
cd whomst
```

2. Run the setup script
```bash
pip install -e .
```

3. Try it out!
```bash
#
```

 ---
# procedure
1. Create a search expression for a recursive level-down tree walking
2. Search files with regex for:
  - `import {{}}`
  - `import {{}} as {{}}`
  - `from {{}} import {{}}`
  - `from {{}} import {{}} as {{}}`
3. Clean results
4. Format output
---
### Path and Tree
```
# build a reference point from current directory
# only include files *.py
# flat-out exclude __pycache__ from search
# return an iterable result
```

### Regex Search
```
# gather result of all lines containing `import`
# some of these lines may extend multiple lines, if so gather everything until parenthesis closes
# return an iterable result
```

### Clean Results
```
#
#

```

### Format Output
```
# figure out if output should be printed to console, or a requirements.txt file
# do it

```
