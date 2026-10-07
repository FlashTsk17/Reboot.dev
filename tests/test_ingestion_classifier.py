from services.ingestion.repository_ingestor import build_snapshot
from services.analysis.classifier import classify

def test_build_snapshot_filters_generated_paths():
    repo = {"owner": {"login": "FlashTsk17"}, "name": "Demo", "full_name": "FlashTsk17/Demo", "default_branch": "main"}
    tree = {"tree": [{"path": "src/app.ts", "type": "blob", "size": 20, "sha": "a"}, {"path": "node_modules/x.js", "type": "blob", "size": 10, "sha": "b"}, {"path": "README.md", "type": "blob", "size": 10, "sha": "c"}]}
    snapshot = build_snapshot(repo, tree, "main", "abc")
    assert [f.path for f in snapshot.files] == ["src/app.ts", "README.md"]
    assert snapshot.stats["total_files"] == 2

def test_classifier_is_deterministic_and_explainable():
    result = classify("backend/src/server.ts")
    assert result.category == "SOURCE"
    assert result.language == "TypeScript"
    assert result.layer == "BACKEND"
    assert result.reasons

def test_test_files_are_prioritized():
    result = classify("backend/src/scoring.test.ts")
    assert result.category == "TEST"
    assert result.layer == "TEST"
    assert result.importance == "HIGH"
