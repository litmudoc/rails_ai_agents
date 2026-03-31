"""Persistent state tracking for already-seen Sentry issues."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone


@dataclass
class MonitorState:
    last_poll: str | None = None
    seen_issues: dict[str, str] = field(default_factory=dict)

    @classmethod
    def load(cls, path: str) -> MonitorState:
        """Load state from a JSON file. Returns empty state if file missing or corrupted."""
        if not os.path.isfile(path):
            return cls()

        try:
            with open(path) as f:
                data = json.load(f)
            return cls(
                last_poll=data.get("last_poll"),
                seen_issues=data.get("seen_issues", {}),
            )
        except (json.JSONDecodeError, OSError, KeyError):
            return cls()

    def save(self, path: str) -> None:
        """Save state to a JSON file. Creates parent directories if needed."""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as f:
            json.dump(
                {"last_poll": self.last_poll, "seen_issues": self.seen_issues},
                f,
                indent=2,
            )

    def is_new(self, issue_id: str, last_seen: str) -> bool:
        """Check if an issue is new or has new events since last seen."""
        if issue_id not in self.seen_issues:
            return True
        return last_seen > self.seen_issues[issue_id]

    def mark_seen(self, issue_id: str, last_seen: str) -> None:
        """Mark an issue as seen with its last_seen timestamp."""
        self.seen_issues[issue_id] = last_seen

    def prune(self, max_age_days: int = 30) -> int:
        """Remove issues older than max_age_days. Returns number of pruned entries."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=max_age_days)).isoformat()
        old_ids = [
            issue_id for issue_id, last_seen in self.seen_issues.items() if last_seen < cutoff
        ]
        for issue_id in old_ids:
            del self.seen_issues[issue_id]
        return len(old_ids)

    @property
    def was_corrupted(self) -> bool:
        """Check if this is a fresh state (possibly from corruption recovery)."""
        return self.last_poll is None and len(self.seen_issues) == 0
