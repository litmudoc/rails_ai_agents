"""Configuration loader for the Sentry MCP server."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class SentryConfig:
    auth_token: str
    org: str
    project: str
    base_url: str = "https://sentry.io/api/0"

    @classmethod
    def from_env(cls) -> SentryConfig:
        # Load .env from the project root (walk up from this file)
        project_root = Path(__file__).resolve().parent.parent
        load_dotenv(project_root / ".env")

        auth_token = os.environ.get("SENTRY_AUTH_TOKEN", "")
        org = os.environ.get("SENTRY_ORG", "")
        project = os.environ.get("SENTRY_PROJECT", "")

        missing = []
        if not auth_token:
            missing.append("SENTRY_AUTH_TOKEN")
        if not org:
            missing.append("SENTRY_ORG")
        if not project:
            missing.append("SENTRY_PROJECT")

        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}. "
                "Set them before starting the MCP server."
            )

        base_url = os.environ.get("SENTRY_BASE_URL", "https://sentry.io/api/0")
        return cls(auth_token=auth_token, org=org, project=project, base_url=base_url)
