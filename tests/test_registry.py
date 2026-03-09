from pathlib import Path

from io_career.source_registry import SourceRegistry


def test_source_registry_validation_has_no_errors():
    root = Path(__file__).resolve().parents[1]
    assert SourceRegistry(root).validate() == []
