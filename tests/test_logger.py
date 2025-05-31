import os
import json
from pathlib import Path
import warehouse.logger as logger
from warehouse.logger import log_event, log_undo_action

def test_log_event_creates_entry(tmp_path, monkeypatch):
    log_file = tmp_path / "activity.log"

    # Patch the LOG_FILE constant inside the logger module
    monkeypatch.setattr(logger, "LOG_FILE", str(log_file))

    log_event("test", "logger_test", language="python", details={"source": "unit"})

    with open(log_file, "r") as f:
        entry = json.loads(f.readline())

    assert entry["action"] == "test"
    assert entry["name"] == "logger_test"
    assert entry["language"] == "python"
    assert entry["details"]["source"] == "unit"

def test_log_undo_action_creates_file(tmp_path, monkeypatch):
    undo_dir = tmp_path / "undo_logs"

    # Patch the UNDO_LOG_DIR inside the logger module
    monkeypatch.setattr(logger, "UNDO_LOG_DIR", str(undo_dir))

    log_undo_action(
        action_type="delete",
        language="python",
        filename="snippet.json",
        snapshot_before={"code": "print('undo')"}
    )

    logs = list(undo_dir.glob("*.json"))
    assert len(logs) == 1

    with open(logs[0], "r") as f:
        data = json.load(f)

    assert data["action_type"] == "delete"
    assert data["language"] == "python"
    assert data["filename"] == "snippet.json"
    assert data["snapshot_before"]["code"] == "print('undo')"

