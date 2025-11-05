"""Testes para CommandExecutor."""
from __future__ import annotations

import sys
import asyncio

import pytest

from app.core.executor import (
    CommandExecutor,
    CommandExecutionError,
    CommandTimeoutError,
)


def python_cmd(*code_lines: str) -> list[str]:
    return [sys.executable, "-c", "; ".join(code_lines)]


def test_run_success():
    result = CommandExecutor.run(
        python_cmd("print('ok')"),
        timeout=5,
    )
    assert result.stdout.strip() == "ok"
    assert result.returncode == 0


def test_run_failure():
    with pytest.raises(CommandExecutionError):
        CommandExecutor.run(
            python_cmd("import sys", "sys.exit(1)"),
            timeout=5,
        )


def test_run_timeout():
    with pytest.raises(CommandTimeoutError):
        CommandExecutor.run(
            python_cmd("import time", "time.sleep(1)"),
            timeout=0.1,
        )


def test_run_type_error():
    with pytest.raises(TypeError):
        CommandExecutor.run("python -c 'print(1)'")  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_run_async_success():
    stdout, stderr = await CommandExecutor.run_async(
        python_cmd("print('async ok')")
    )
    assert stdout.strip() == "async ok"
    assert stderr.strip() == ""


@pytest.mark.asyncio
async def test_run_async_failure():
    with pytest.raises(CommandExecutionError):
        await CommandExecutor.run_async(
            python_cmd("import sys", "sys.exit(2)")
        )


@pytest.mark.asyncio
async def test_run_async_timeout():
    with pytest.raises(CommandTimeoutError):
        await CommandExecutor.run_async(
            python_cmd("import time", "time.sleep(1)"),
            timeout=0.1,
        )


@pytest.mark.asyncio
async def test_run_async_type_error():
    with pytest.raises(TypeError):
        await CommandExecutor.run_async("python -c 'print(1)'")  # type: ignore[arg-type]
