# whomst :owl:
#### mystery dependency detective & missing `requirements.txt` creator
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
### `/usr/bin`
```bash
git clone https://github.com/minelminel/whomst.git
cd whomst
./install
```

### `/site-packages/`
```bash
git clone https://github.com/minelminel/whomst.git
cd whomst
pip install -e .
```

### Uninstall
```bash
cd whomst && ./uninstall
```
