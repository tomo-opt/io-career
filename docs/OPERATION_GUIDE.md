# Operation Guide

```bash
pip install -r requirements.txt
pip install -e .
python -m io_career.main validate-sources
python -m io_career.main run
python -m io_career.main export-site
python -m io_career.main compare
```

Notes:
- `data/processed/latest/` and `site/data/jobs.json` are cumulative (historical + newly discovered).
- `data/processed/daily_new/` is daily incremental only.
