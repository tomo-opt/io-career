# Architecture

- `source_registry.py`: source loading and validation.
- `fetchers/http_client.py`: HTTP with retries/backoff.
- `parsers/common.py`: parser strategies and normalization.
- `pipeline/engine.py`: source crawling + error capture.
- `pipeline/diff.py`: daily new-position detection.
- `pipeline/exporters.py`: output and site export.
- `main.py`: CLI entrypoint.
