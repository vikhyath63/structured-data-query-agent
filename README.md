# Structured Data Query Agent

A safe query API for JSON records and CSV files. It detects available fields and supports allow-listed filtering, sorting and aggregation—without executing generated Python or SQL.

## Run
```bash
pip install -e ".[dev]"
uvicorn app.main:app --reload
```
Use POST /query with a records array, a filter object and an optional aggregation. See /docs.
