# io-career

Global IO internship and early-career crawler with daily diff, archives, and GitHub Pages dashboard.

Data logic:
- Main dataset and website show the cumulative full set of all records ever crawled (`latest/jobs.*` + `site/data/jobs.json`).
- Daily incremental output is separated in `data/processed/daily_new/YYYY-MM-DD_new_positions.txt`.

## Quickstart
```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
pip install -r requirements.txt
pip install -e .
python -m io_career.main validate-sources
python -m io_career.main run
python -m io_career.main export-site
```

## CLI
```bash
python -m io_career.main run
python -m io_career.main validate-sources
python -m io_career.main export-site
python -m io_career.main compare
```

## Outputs
- `data/processed/latest/`
- `data/processed/daily_new/`
- `data/archive/`
- `site/data/`
