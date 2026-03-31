"""Tests for PII redaction."""

from __future__ import annotations

from mcp_server.redactor import redact_event
from tests.conftest import MOCK_LATEST_EVENT


class TestRedactEvent:
    def test_strips_user_context(self):
        result = redact_event(MOCK_LATEST_EVENT)
        assert "user" not in result
        assert result["pii_redacted"] is True

    def test_strips_request_headers(self):
        result = redact_event(MOCK_LATEST_EVENT)
        for entry in result["entries"]:
            if entry.get("type") == "request":
                assert "headers" not in entry["data"]
                assert "data" not in entry["data"]
                assert "query_string" not in entry["data"]
                # URL and method should be preserved
                assert entry["data"]["url"] == "https://myapp.com/payments"
                assert entry["data"]["method"] == "POST"

    def test_strips_frame_vars(self):
        result = redact_event(MOCK_LATEST_EVENT)
        for entry in result["entries"]:
            if entry.get("type") == "exception":
                for exc_val in entry["data"]["values"]:
                    for frame in exc_val["stacktrace"]["frames"]:
                        assert "vars" not in frame

    def test_strips_breadcrumb_data(self):
        result = redact_event(MOCK_LATEST_EVENT)
        for entry in result["entries"]:
            if entry.get("type") == "breadcrumbs":
                for crumb in entry["data"]["values"]:
                    assert "data" not in crumb

    def test_preserves_safe_fields(self):
        result = redact_event(MOCK_LATEST_EVENT)
        # Tags preserved
        assert len(result["tags"]) == 3
        # Contexts preserved
        assert result["contexts"]["runtime"]["name"] == "Ruby"
        # Exception type/value preserved
        for entry in result["entries"]:
            if entry.get("type") == "exception":
                exc = entry["data"]["values"][0]
                assert exc["type"] == "TypeError"
                assert exc["value"] == "Cannot read property 'x' of undefined"
                # Filename, function, lineNo preserved
                frame = exc["stacktrace"]["frames"][0]
                assert frame["filename"] == "/app/services/payment_service.rb"
                assert frame["function"] == "process_payment"
                assert frame["lineNo"] == 42

    def test_adds_pii_note(self):
        result = redact_event(MOCK_LATEST_EVENT)
        assert "pii_note" in result
        assert "include_pii=True" in result["pii_note"]

    def test_include_pii_preserves_all(self):
        result = redact_event(MOCK_LATEST_EVENT, include_pii=True)
        assert result["pii_redacted"] is False
        assert result["user"]["email"] == "john@example.com"
        # Frame vars preserved
        for entry in result["entries"]:
            if entry.get("type") == "exception":
                frame = entry["data"]["values"][0]["stacktrace"]["frames"][0]
                assert "vars" in frame
        # Request data preserved
        for entry in result["entries"]:
            if entry.get("type") == "request":
                assert "headers" in entry["data"]
                assert "data" in entry["data"]

    def test_does_not_mutate_original(self):
        original_user = MOCK_LATEST_EVENT["user"]["email"]
        redact_event(MOCK_LATEST_EVENT)
        assert MOCK_LATEST_EVENT["user"]["email"] == original_user

    def test_handles_missing_fields(self):
        minimal_event = {"entries": [], "tags": []}
        result = redact_event(minimal_event)
        assert result["pii_redacted"] is True

    def test_handles_empty_event(self):
        result = redact_event({})
        assert result["pii_redacted"] is True
