# whomst :owl:
[![Build Status](https://travis-ci.org/minelminel/whomst.svg?branch=master)](https://travis-ci.org/minelminel/whomst)
[![codecov](https://codecov.io/gh/minelminel/whomst/branch/master/graph/badge.svg)](https://codecov.io/gh/minelminel/whomst)
#### mystery dependency detective & missing `requirements.txt` creator
---
### now on PyPI!!! 🤗 `pip install whomst`
---

```
🦉 ~/whomst:$  whomst .
bar
foo
new
pytest
setuptools
whomst

🦉 ~/whomst:$  whomst . > requirements.txt

🦉 ~/whomst:$  whomst . > requirements.txt && cat requirements.txt
bar
foo
new
pytest
setuptools
whomst
```
---
### Install from source
```bash
git clone https://github.com/minelminel/whomst.git
cd whomst
pip install -e .
```
