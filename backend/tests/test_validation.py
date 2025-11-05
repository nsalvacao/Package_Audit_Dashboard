"""Testes para ValidationLayer."""
from __future__ import annotations

import pytest
from pathlib import Path

from app.core.validation import (
    ValidationLayer,
    InvalidPackageNameError,
    PathTraversalError,
)


@pytest.fixture(autouse=True)
def patch_allowed_base_dir(tmp_path):
    base = tmp_path / ".package-audit"
    ValidationLayer.ALLOWED_BASE_DIR = base
    return base


class TestPackageNameSanitization:
    def test_valid_simple_name(self):
        assert ValidationLayer.sanitize_package_name("react") == "react"

    def test_valid_scoped_name(self):
        assert ValidationLayer.sanitize_package_name("@types/node") == "@types/node"

    def test_valid_with_hyphen(self):
        assert ValidationLayer.sanitize_package_name("lodash-es") == "lodash-es"

    def test_valid_with_underscore(self):
        assert ValidationLayer.sanitize_package_name("test_package") == "test_package"

    def test_reject_shell_injection(self):
        with pytest.raises(InvalidPackageNameError):
            ValidationLayer.sanitize_package_name("lodash; rm -rf /")

    def test_reject_pipe_injection(self):
        with pytest.raises(InvalidPackageNameError):
            ValidationLayer.sanitize_package_name("lodash | cat /etc/passwd")

    def test_reject_path_traversal_in_name(self):
        with pytest.raises(InvalidPackageNameError):
            ValidationLayer.sanitize_package_name("../../etc/passwd")

    def test_reject_empty_name(self):
        with pytest.raises(InvalidPackageNameError):
            ValidationLayer.sanitize_package_name("")

    def test_reject_too_long_name(self):
        long_name = "a" * 300
        with pytest.raises(InvalidPackageNameError):
            ValidationLayer.sanitize_package_name(long_name)

    def test_reject_special_characters(self):
        invalid_names = [
            "package$name",
            "package#name",
            "package name",
            "package\nname",
            "package;name",
        ]
        for name in invalid_names:
            with pytest.raises(InvalidPackageNameError):
                ValidationLayer.sanitize_package_name(name)


class TestCommandBuilding:
    def test_build_simple_command(self):
        cmd = ValidationLayer.build_safe_command(["npm", "uninstall"], ["react"])
        assert cmd == ["npm", "uninstall", "react"]
        assert isinstance(cmd, list)

    def test_build_multiple_args(self):
        cmd = ValidationLayer.build_safe_command(
            ["npm", "install"],
            ["react", "vue", "angular"],
        )
        assert cmd == ["npm", "install", "react", "vue", "angular"]

    def test_reject_invalid_arg(self):
        with pytest.raises(InvalidPackageNameError):
            ValidationLayer.build_safe_command(
                ["npm", "install"],
                ["react", "lodash; rm -rf /"],
            )

    def test_require_list_base_cmd(self):
        with pytest.raises(TypeError):
            ValidationLayer.build_safe_command("npm install", ["react"])

    def test_require_list_args(self):
        with pytest.raises(TypeError):
            ValidationLayer.build_safe_command(["npm", "install"], "react")


class TestPathValidation:
    def test_valid_relative_path(self, patch_allowed_base_dir):
        path = ValidationLayer.validate_path("snapshots/test.json")
        expected = patch_allowed_base_dir / "snapshots" / "test.json"
        assert path == expected.resolve()
        assert isinstance(path, Path)

    def test_valid_absolute_path(self, patch_allowed_base_dir):
        absolute = (patch_allowed_base_dir / "snapshots" / "test.json").resolve()
        absolute.parent.mkdir(parents=True, exist_ok=True)
        result = ValidationLayer.validate_path(str(absolute))
        assert result == absolute

    def test_reject_traversal_up(self):
        with pytest.raises(PathTraversalError):
            ValidationLayer.validate_path("../../etc/passwd")

    def test_reject_absolute_outside(self, tmp_path):
        outside = tmp_path / "other" / "file.json"
        outside.parent.mkdir(parents=True, exist_ok=True)
        with pytest.raises(PathTraversalError):
            ValidationLayer.validate_path(str(outside))


class TestManagerIdSanitization:
    def test_valid_simple_id(self):
        assert ValidationLayer.sanitize_manager_id("npm") == "npm"

    def test_valid_with_hyphen(self):
        assert ValidationLayer.sanitize_manager_id("pip-tools") == "pip-tools"

    def test_reject_uppercase(self):
        with pytest.raises(InvalidPackageNameError):
            ValidationLayer.sanitize_manager_id("NPM")

    def test_reject_special_chars(self):
        with pytest.raises(InvalidPackageNameError):
            ValidationLayer.sanitize_manager_id("npm;rm")

    def test_reject_too_long(self):
        with pytest.raises(InvalidPackageNameError):
            ValidationLayer.sanitize_manager_id("a" * 100)
