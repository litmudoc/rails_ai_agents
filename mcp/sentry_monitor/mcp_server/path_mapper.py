"""Map Sentry stack trace file paths to local repository files."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass


DEPLOY_PREFIXES = [
    r"^/app/",
    r"^/home/[^/]+/",
    r"^/var/www/[^/]+/",
    r"^/srv/[^/]+/",
    r"^/opt/[^/]+/",
]


@dataclass
class FrameMapping:
    sentry_path: str
    local_path: str | None
    confidence: str  # "exact", "partial", "unmapped"
    line_no: int | None
    exists: bool


def _strip_deploy_prefix(path: str) -> str:
    """Remove common deployment prefixes from a file path."""
    for prefix_pattern in DEPLOY_PREFIXES:
        stripped = re.sub(prefix_pattern, "", path)
        if stripped != path:
            return stripped
    return path.lstrip("/")


def _find_file_in_repo(relative_path: str, repo_root: str) -> tuple[str | None, str]:
    """Search for a file in the repo. Returns (absolute_path, confidence)."""
    # Try exact relative path
    candidate = os.path.join(repo_root, relative_path)
    if os.path.isfile(candidate):
        return candidate, "exact"

    # Try filename-only search (partial match)
    filename = os.path.basename(relative_path)
    for dirpath, _dirs, files in os.walk(repo_root):
        # Skip hidden directories and common non-source dirs
        rel_dir = os.path.relpath(dirpath, repo_root)
        if any(
            part.startswith(".") or part in ("node_modules", "vendor", "__pycache__", ".venv")
            for part in rel_dir.split(os.sep)
        ):
            continue
        if filename in files:
            return os.path.join(dirpath, filename), "partial"

    return None, "unmapped"


def map_frames_to_local(frames: list[dict], repo_root: str) -> list[FrameMapping]:
    """Map a list of Sentry stack trace frames to local files."""
    if not os.path.isdir(repo_root):
        raise ValueError(f"Repository root not found: {repo_root}")

    mappings = []
    for frame in frames:
        sentry_path = frame.get("filename", "")
        line_no = frame.get("lineNo")

        relative = _strip_deploy_prefix(sentry_path)
        local_path, confidence = _find_file_in_repo(relative, repo_root)

        mappings.append(
            FrameMapping(
                sentry_path=sentry_path,
                local_path=local_path,
                confidence=confidence,
                line_no=line_no,
                exists=local_path is not None,
            )
        )

    return mappings


def format_mapping_summary(mappings: list[FrameMapping]) -> str:
    """Generate a human-readable summary of mapping results."""
    total = len(mappings)
    exact = sum(1 for m in mappings if m.confidence == "exact")
    partial = sum(1 for m in mappings if m.confidence == "partial")
    unmapped = sum(1 for m in mappings if m.confidence == "unmapped")
    mapped = exact + partial

    parts = []
    if exact:
        parts.append(f"{exact} exact")
    if partial:
        parts.append(f"{partial} partial")
    if unmapped:
        parts.append(f"{unmapped} unmapped")

    return f"{mapped}/{total} frames mapped ({', '.join(parts)})"
