"""Executor seguro de comandos do sistema."""
from __future__ import annotations

import asyncio
import logging
import subprocess
from typing import List, Optional, Tuple


logger = logging.getLogger(__name__)


class CommandTimeoutError(Exception):
    """Comando ultrapassou o tempo limite."""


class CommandExecutionError(Exception):
    """Comando terminou com erro."""


class CommandExecutor:
    """Wrapper que garante execuções seguras e auditáveis."""

    DEFAULT_TIMEOUT = 30

    @staticmethod
    def run(
        command: List[str],
        timeout: Optional[int] = None,
        check: bool = True,
        cwd: Optional[str] = None,
    ) -> subprocess.CompletedProcess:
        if not isinstance(command, list):
            raise TypeError("Command must be provided as a list.")

        timeout = timeout or CommandExecutor.DEFAULT_TIMEOUT
        logger.info("Executing command: %s", " ".join(command))

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=check,
                cwd=cwd,
            )
            logger.info("Command finished with code %s", result.returncode)
            return result

        except subprocess.TimeoutExpired as exc:
            logger.error("Command timed out after %s seconds", timeout)
            raise CommandTimeoutError(
                f"Command timed out after {timeout}s: {command[0]}"
            ) from exc
        except subprocess.CalledProcessError as exc:
            logger.error("Command failed: %s", exc.stderr.strip())
            raise CommandExecutionError(
                f"Command failed (exit {exc.returncode}): {exc.stderr.strip()}"
            ) from exc

    @staticmethod
    async def run_async(
        command: List[str],
        timeout: Optional[int] = None,
    ) -> Tuple[str, str]:
        if not isinstance(command, list):
            raise TypeError("Command must be provided as a list.")

        timeout = timeout or CommandExecutor.DEFAULT_TIMEOUT
        logger.info("Executing async command: %s", " ".join(command))

        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout,
            )
        except asyncio.TimeoutError as exc:
            process.kill()
            try:
                await process.wait()
            except ProcessLookupError:
                pass
            logger.error("Async command timed out after %s seconds", timeout)
            raise CommandTimeoutError(
                f"Command timed out after {timeout}s: {command[0]}"
            ) from exc

        stdout_text = stdout.decode()
        stderr_text = stderr.decode()

        if process.returncode != 0:
            logger.error("Async command failed: %s", stderr_text.strip())
            raise CommandExecutionError(
                f"Command failed (exit {process.returncode}): {stderr_text.strip()}"
            )

        logger.info("Async command finished with code %s", process.returncode)
        return stdout_text, stderr_text
