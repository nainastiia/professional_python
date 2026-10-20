
# Lab 06 — Variant 10: Warehouse stock management

Self-contained example for automated testing. Not the original Lab_01 code.

## Run

```bash
python -m pip install -e ".[dev]"
python -m pytest -v --cov=warehouse --cov-branch --cov-report=term-missing --cov-report=html
```

Open `htmlcov/index.html` for the coverage report.
