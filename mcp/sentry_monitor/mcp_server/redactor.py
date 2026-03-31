"""PII redaction for Sentry event data."""

from __future__ import annotations

import copy

PII_NOTE = (
    "User context, request headers/body, local variables, and breadcrumb data were redacted. "
    "Use include_pii=True to see full context."
)


def redact_event(event_data: dict, include_pii: bool = False) -> dict:
    """Strip PII fields from a Sentry event. Returns a new dict (no mutation)."""
    result = copy.deepcopy(event_data)

    if include_pii:
        result["pii_redacted"] = False
        return result

    # Strip user object
    result.pop("user", None)

    # Strip request entry data
    for entry in result.get("entries", []):
        if entry.get("type") == "request":
            data = entry.get("data", {})
            data.pop("headers", None)
            data.pop("data", None)
            data.pop("query_string", None)

        # Strip breadcrumb data
        if entry.get("type") == "breadcrumbs":
            for crumb in entry.get("data", {}).get("values", []):
                crumb.pop("data", None)

        # Strip local variables from stack frames
        if entry.get("type") == "exception":
            for exc_value in entry.get("data", {}).get("values", []):
                frames = exc_value.get("stacktrace", {}).get("frames", [])
                for frame in frames:
                    frame.pop("vars", None)

    result["pii_redacted"] = True
    result["pii_note"] = PII_NOTE

    return result
