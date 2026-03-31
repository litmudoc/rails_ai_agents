"""Tests for stack trace path mapping."""

from __future__ import annotations

import os
import tempfile

import pytest

from mcp_server.path_mapper import (
    _strip_deploy_prefix,
    format_mapping_summary,
    map_frames_to_local,
)


class TestStripDeployPrefix:
    def test_strips_app_prefix(self):
        assert _strip_deploy_prefix("/app/services/foo.rb") == "services/foo.rb"

    def test_strips_home_prefix(self):
        assert _strip_deploy_prefix("/home/deploy/services/foo.rb") == "services/foo.rb"

    def test_strips_var_www_prefix(self):
        assert _strip_deploy_prefix("/var/www/myapp/services/foo.rb") == "services/foo.rb"

    def test_no_prefix_strips_leading_slash(self):
        assert _strip_deploy_prefix("/services/foo.rb") == "services/foo.rb"

    def test_relative_path_unchanged(self):
        assert _strip_deploy_prefix("services/foo.rb") == "services/foo.rb"


class TestMapFramesToLocal:
    def test_exact_match(self):
        with tempfile.TemporaryDirectory() as repo:
            os.makedirs(os.path.join(repo, "app", "services"))
            target = os.path.join(repo, "app", "services", "payment_service.rb")
            with open(target, "w") as f:
                f.write("# test")

            frames = [{"filename": "/app/app/services/payment_service.rb", "lineNo": 42}]
            mappings = map_frames_to_local(frames, repo)

            assert len(mappings) == 1
            assert mappings[0].confidence == "exact"
            assert mappings[0].exists is True
            assert mappings[0].local_path == target

    def test_partial_match(self):
        with tempfile.TemporaryDirectory() as repo:
            os.makedirs(os.path.join(repo, "lib"))
            target = os.path.join(repo, "lib", "helper.rb")
            with open(target, "w") as f:
                f.write("# test")

            frames = [{"filename": "/app/different/path/helper.rb", "lineNo": 10}]
            mappings = map_frames_to_local(frames, repo)

            assert len(mappings) == 1
            assert mappings[0].confidence == "partial"
            assert mappings[0].exists is True

    def test_unmapped(self):
        with tempfile.TemporaryDirectory() as repo:
            frames = [{"filename": "/app/nonexistent/file.rb", "lineNo": 1}]
            mappings = map_frames_to_local(frames, repo)

            assert len(mappings) == 1
            assert mappings[0].confidence == "unmapped"
            assert mappings[0].exists is False
            assert mappings[0].local_path is None

    def test_invalid_repo_root(self):
        with pytest.raises(ValueError, match="Repository root not found"):
            map_frames_to_local([], "/nonexistent/path")

    def test_empty_frames(self):
        with tempfile.TemporaryDirectory() as repo:
            mappings = map_frames_to_local([], repo)
            assert mappings == []


class TestFormatMappingSummary:
    def test_all_exact(self):
        from mcp_server.path_mapper import FrameMapping

        mappings = [
            FrameMapping("/app/a.rb", "/local/a.rb", "exact", 1, True),
            FrameMapping("/app/b.rb", "/local/b.rb", "exact", 2, True),
        ]
        assert format_mapping_summary(mappings) == "2/2 frames mapped (2 exact)"

    def test_mixed(self):
        from mcp_server.path_mapper import FrameMapping

        mappings = [
            FrameMapping("/app/a.rb", "/local/a.rb", "exact", 1, True),
            FrameMapping("/app/b.rb", "/local/b.rb", "partial", 2, True),
            FrameMapping("/app/c.rb", None, "unmapped", 3, False),
        ]
        summary = format_mapping_summary(mappings)
        assert "2/3 frames mapped" in summary
        assert "1 exact" in summary
        assert "1 partial" in summary
        assert "1 unmapped" in summary
