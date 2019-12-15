rm -rf ./build/ ./dist/
python3 setup.py sdist bdist_wheel
twine upload dist/* --non-interactive --verbose
# TWINE_USERNAME, TWINE_PASSWORD env vars
