# Python Programming Guide

Notes and reference for Python 3.14.5 and popular libraries, built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).

**Live site:** https://qgjones9.github.io/python-programming-guide/

## Local development

```bash
source setup.sh
```

Or manually:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

After adding or reorganizing doc sections, regenerate the sidebar:

```bash
./scripts/update_mkdocs_nav.sh
```

## Publishing

Pushes to `main` deploy automatically via [`.github/workflows/deploy-docs.yml`](.github/workflows/deploy-docs.yml). In the repo **Settings → Pages**, set the source to **GitHub Actions**.
