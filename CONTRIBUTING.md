# Contributing

## Build and upload to pypi

Increase version number in `setup.py`

```bash
make upload
# Upgrade version number before
```
Currently, releasing `gameprices` with the Github Workflow does not work.

## Build locally

```bash
 python3 -m venv .venv
 . .venv/bin/activate
 make test_deps test
```

## Get test coverage

```bash
make coverage
```
