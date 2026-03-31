"""Shared test fixtures for the Sentry MCP server."""

from __future__ import annotations

import pytest
import respx

from mcp_server.config import SentryConfig
from mcp_server.sentry_client import SentryClient


@pytest.fixture
def sentry_config():
    return SentryConfig(
        auth_token="test-token-123",
        org="test-org",
        project="test-project",
        base_url="https://sentry.io/api/0",
    )


@pytest.fixture
def mock_sentry(sentry_config):
    with respx.mock(base_url=sentry_config.base_url) as mock:
        yield mock


@pytest.fixture
async def sentry_client(sentry_config):
    client = SentryClient(sentry_config)
    yield client
    await client.close()


# --- Mock response payloads ---

MOCK_ISSUE_LIST = [
    {
        "id": "12345",
        "shortId": "TEST-PROJECT-1",
        "title": "TypeError: Cannot read property 'x' of undefined",
        "culprit": "app/services/payment_service.rb",
        "status": "unresolved",
        "level": "error",
        "count": "42",
        "userCount": 15,
        "firstSeen": "2026-03-28T10:00:00Z",
        "lastSeen": "2026-03-31T09:55:00Z",
        "project": {"id": "1", "name": "test-project", "slug": "test-project"},
        "metadata": {
            "type": "TypeError",
            "value": "Cannot read property 'x' of undefined",
            "filename": "app/services/payment_service.rb",
            "function": "process_payment",
        },
        "permalink": "https://sentry.io/organizations/test-org/issues/12345/",
    },
    {
        "id": "12346",
        "shortId": "TEST-PROJECT-2",
        "title": "NoMethodError: undefined method 'save!'",
        "culprit": "app/models/user.rb",
        "status": "unresolved",
        "level": "error",
        "count": "7",
        "userCount": 3,
        "firstSeen": "2026-03-30T14:00:00Z",
        "lastSeen": "2026-03-31T10:05:00Z",
        "project": {"id": "1", "name": "test-project", "slug": "test-project"},
        "metadata": {
            "type": "NoMethodError",
            "value": "undefined method 'save!'",
            "filename": "app/models/user.rb",
            "function": "create_user",
        },
        "permalink": "https://sentry.io/organizations/test-org/issues/12346/",
    },
]

MOCK_ISSUE_DETAIL = {
    "id": "12345",
    "shortId": "TEST-PROJECT-1",
    "title": "TypeError: Cannot read property 'x' of undefined",
    "culprit": "app/services/payment_service.rb",
    "status": "unresolved",
    "level": "error",
    "count": "42",
    "userCount": 15,
    "firstSeen": "2026-03-28T10:00:00Z",
    "lastSeen": "2026-03-31T09:55:00Z",
    "project": {"id": "1", "name": "test-project", "slug": "test-project"},
    "permalink": "https://sentry.io/organizations/test-org/issues/12345/",
}

MOCK_LATEST_EVENT = {
    "eventID": "evt-abc123",
    "dateCreated": "2026-03-31T09:55:00Z",
    "entries": [
        {
            "type": "exception",
            "data": {
                "values": [
                    {
                        "type": "TypeError",
                        "value": "Cannot read property 'x' of undefined",
                        "stacktrace": {
                            "frames": [
                                {
                                    "filename": "/app/services/payment_service.rb",
                                    "function": "process_payment",
                                    "lineNo": 42,
                                    "context": [
                                        [40, "  def process_payment"],
                                        [41, "    amount = params[:amount]"],
                                        [42, "    result = gateway.charge(amount)"],
                                        [43, "    result.x"],
                                        [44, "  end"],
                                    ],
                                    "vars": {
                                        "amount": "100",
                                        "user_email": "john@example.com",
                                    },
                                },
                                {
                                    "filename": "/app/controllers/payments_controller.rb",
                                    "function": "create",
                                    "lineNo": 15,
                                    "context": [
                                        [14, "  def create"],
                                        [15, "    PaymentService.new.process_payment(params)"],
                                        [16, "  end"],
                                    ],
                                    "vars": {"params": "{'amount': '100'}"},
                                },
                            ]
                        },
                    }
                ]
            },
        },
        {
            "type": "breadcrumbs",
            "data": {
                "values": [
                    {
                        "category": "http",
                        "data": {"url": "https://api.stripe.com/v1/charges?token=sk_test_123"},
                        "timestamp": "2026-03-31T09:54:59Z",
                    }
                ]
            },
        },
        {
            "type": "request",
            "data": {
                "url": "https://myapp.com/payments",
                "method": "POST",
                "headers": [
                    ["Cookie", "session=abc123secret"],
                    ["Authorization", "Bearer user-token-456"],
                    ["Content-Type", "application/json"],
                ],
                "data": {"card_number": "4242424242424242", "amount": "100"},
                "query_string": "ref=checkout&user_id=789",
            },
        },
    ],
    "tags": [
        {"key": "environment", "value": "production"},
        {"key": "level", "value": "error"},
        {"key": "browser", "value": "Chrome 120"},
    ],
    "contexts": {
        "os": {"name": "macOS", "version": "14.0"},
        "runtime": {"name": "Ruby", "version": "3.3.6"},
    },
    "user": {
        "id": "789",
        "email": "john@example.com",
        "ip_address": "192.168.1.100",
        "username": "johndoe",
    },
}

LINK_HEADER_WITH_NEXT = (
    "<https://sentry.io/api/0/projects/test-org/test-project/issues/?cursor=abc123>; "
    'rel="previous"; results="false"; cursor="abc123", '
    "<https://sentry.io/api/0/projects/test-org/test-project/issues/?cursor=def456>; "
    'rel="next"; results="true"; cursor="def456"'
)

LINK_HEADER_NO_NEXT = (
    "<https://sentry.io/api/0/projects/test-org/test-project/issues/?cursor=abc123>; "
    'rel="previous"; results="false"; cursor="abc123", '
    "<https://sentry.io/api/0/projects/test-org/test-project/issues/?cursor=def456>; "
    'rel="next"; results="false"; cursor="def456"'
)
