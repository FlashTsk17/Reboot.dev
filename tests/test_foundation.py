from pathlib import Path

def test_core_directories_exist():
    expected = [
        "apps/api", "packages/core", "services/ingestion",
        "services/analysis", "services/diagnosis", "services/priority",
        "services/rescan", "docs", "tests",
    ]
    for path in expected:
        assert Path(path).is_dir()
