"""Tests for monitoring state persistence."""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone

from mcp_server.state import MonitorState


class TestLoad:
    def test_load_missing_file(self, tmp_path):
        state = MonitorState.load(str(tmp_path / "nonexistent.json"))
        assert state.last_poll is None
        assert state.seen_issues == {}

    def test_load_empty_file(self, tmp_path):
        path = tmp_path / "state.json"
        path.write_text("")
        state = MonitorState.load(str(path))
        assert state.last_poll is None
        assert state.seen_issues == {}

    def test_load_corrupted_json(self, tmp_path):
        path = tmp_path / "state.json"
        path.write_text("{invalid json!!!")
        state = MonitorState.load(str(path))
        assert state.last_poll is None
        assert state.seen_issues == {}

    def test_load_valid_state(self, tmp_path):
        path = tmp_path / "state.json"
        path.write_text(
            json.dumps(
                {
                    "last_poll": "2026-03-31T10:00:00Z",
                    "seen_issues": {"123": "2026-03-31T09:55:00Z"},
                }
            )
        )
        state = MonitorState.load(str(path))
        assert state.last_poll == "2026-03-31T10:00:00Z"
        assert state.seen_issues == {"123": "2026-03-31T09:55:00Z"}


class TestSaveAndRoundTrip:
    def test_save_creates_file(self, tmp_path):
        path = str(tmp_path / "subdir" / "state.json")
        state = MonitorState(
            last_poll="2026-03-31T10:00:00Z",
            seen_issues={"123": "2026-03-31T09:55:00Z"},
        )
        state.save(path)
        assert os.path.isfile(path)

    def test_round_trip(self, tmp_path):
        path = str(tmp_path / "state.json")
        original = MonitorState(
            last_poll="2026-03-31T10:00:00Z",
            seen_issues={"123": "2026-03-31T09:55:00Z", "456": "2026-03-31T09:50:00Z"},
        )
        original.save(path)
        loaded = MonitorState.load(path)
        assert loaded.last_poll == original.last_poll
        assert loaded.seen_issues == original.seen_issues


class TestIsNew:
    def test_unseen_issue(self):
        state = MonitorState(seen_issues={})
        assert state.is_new("123", "2026-03-31T10:00:00Z") is True

    def test_previously_seen_no_new_events(self):
        state = MonitorState(seen_issues={"123": "2026-03-31T10:00:00Z"})
        assert state.is_new("123", "2026-03-31T09:00:00Z") is False

    def test_previously_seen_with_new_events(self):
        state = MonitorState(seen_issues={"123": "2026-03-31T09:00:00Z"})
        assert state.is_new("123", "2026-03-31T10:00:00Z") is True


class TestMarkSeen:
    def test_marks_new_issue(self):
        state = MonitorState()
        state.mark_seen("123", "2026-03-31T10:00:00Z")
        assert state.seen_issues["123"] == "2026-03-31T10:00:00Z"

    def test_updates_existing_issue(self):
        state = MonitorState(seen_issues={"123": "2026-03-31T09:00:00Z"})
        state.mark_seen("123", "2026-03-31T10:00:00Z")
        assert state.seen_issues["123"] == "2026-03-31T10:00:00Z"


class TestPrune:
    def test_removes_old_entries(self):
        old_time = (datetime.now(timezone.utc) - timedelta(days=31)).isoformat()
        recent_time = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()

        state = MonitorState(seen_issues={"old": old_time, "recent": recent_time})
        pruned = state.prune(max_age_days=30)

        assert pruned == 1
        assert "old" not in state.seen_issues
        assert "recent" in state.seen_issues

    def test_no_pruning_needed(self):
        recent_time = datetime.now(timezone.utc).isoformat()
        state = MonitorState(seen_issues={"123": recent_time})
        pruned = state.prune()
        assert pruned == 0
        assert "123" in state.seen_issues


class TestWasCorrupted:
    def test_fresh_state_is_flagged(self):
        state = MonitorState()
        assert state.was_corrupted is True

    def test_populated_state_is_not_flagged(self):
        state = MonitorState(last_poll="2026-03-31T10:00:00Z")
        assert state.was_corrupted is False
