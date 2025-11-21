"""Host Command Executor - Execute commands on the host system from Docker container."""
from __future__ import annotations

import logging
import os
import subprocess
from enum import Enum
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)


class HostExecutionMode(str, Enum):
    """Available host execution modes."""
    
    DOCKER = "docker"  # Execute on host via Docker socket
    SSH = "ssh"  # Execute on host via SSH
    DIRECT = "direct"  # Direct execution (when running natively)


class HostExecutionError(Exception):
    """Error executing command on host."""
    pass


class HostCommandExecutor:
    """Execute commands on the host system from within a Docker container."""
    
    DEFAULT_TIMEOUT = 60
    
    def __init__(self):
        """Initialize host executor with environment configuration."""
        self.enabled = os.getenv("ENABLE_HOST_ACCESS", "false").lower() == "true"
        self.mode = HostExecutionMode(os.getenv("HOST_EXECUTION_MODE", "docker"))
        self.ssh_host = os.getenv("SSH_HOST", "host.docker.internal")
        self.ssh_port = int(os.getenv("SSH_PORT", "22"))
        self.ssh_user = os.getenv("SSH_USER", os.getenv("USER", "user"))
        self.ssh_key_path = os.getenv("SSH_KEY_PATH", "/host/.ssh/id_rsa")
        
        logger.info(
            "HostCommandExecutor initialized: enabled=%s, mode=%s",
            self.enabled,
            self.mode.value
        )
    
    def is_enabled(self) -> bool:
        """Check if host access is enabled."""
        return self.enabled
    
    def execute(
        self,
        command: List[str],
        timeout: Optional[int] = None,
        shell: str = "bash",
    ) -> Tuple[str, str, int]:
        """
        Execute a command on the host system.
        
        Args:
            command: Command and arguments as list
            timeout: Timeout in seconds
            shell: Shell to use (bash, powershell, cmd)
            
        Returns:
            Tuple of (stdout, stderr, return_code)
            
        Raises:
            HostExecutionError: If execution fails
        """
        if not self.enabled:
            raise HostExecutionError("Host access is not enabled")
        
        timeout = timeout or self.DEFAULT_TIMEOUT
        
        if self.mode == HostExecutionMode.DOCKER:
            return self._execute_via_docker(command, timeout, shell)
        elif self.mode == HostExecutionMode.SSH:
            return self._execute_via_ssh(command, timeout, shell)
        elif self.mode == HostExecutionMode.DIRECT:
            return self._execute_direct(command, timeout, shell)
        else:
            raise HostExecutionError(f"Unknown execution mode: {self.mode}")
    
    def _execute_direct(
        self,
        command: List[str],
        timeout: int,
        shell: str,
    ) -> Tuple[str, str, int]:
        """Execute command directly (when running natively)."""
        logger.info("Executing command directly: %s", " ".join(command))
        
        try:
            # Use shell execution for proper command interpretation
            if shell == "powershell":
                full_command = ["pwsh", "-Command"] + command
            elif shell == "cmd":
                full_command = ["cmd", "/c"] + command
            else:
                full_command = command
            
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
            
            return result.stdout, result.stderr, result.returncode
            
        except subprocess.TimeoutExpired:
            raise HostExecutionError(f"Command timed out after {timeout}s")
        except Exception as e:
            raise HostExecutionError(f"Failed to execute command: {e}")
    
    def _execute_via_docker(
        self,
        command: List[str],
        timeout: int,
        shell: str,
    ) -> Tuple[str, str, int]:
        """
        Execute command on host via Docker socket.
        
        This method runs a temporary container on the host with host networking
        and necessary volume mounts to execute commands as if on the host.
        """
        logger.info("Executing command via Docker: %s", " ".join(command))
        
        try:
            # Build the docker command to execute on host
            docker_command = [
                "docker", "run",
                "--rm",  # Remove container after execution
                "--network=host",  # Use host networking
                "-v", "/:/host",  # Mount host root filesystem
                "-v", "/var/run/docker.sock:/var/run/docker.sock",  # Docker socket
            ]
            
            # Choose appropriate image based on shell
            if shell == "powershell":
                # Use PowerShell image for Windows commands
                docker_command.extend([
                    "mcr.microsoft.com/powershell:latest",
                    "pwsh", "-Command",
                ])
            elif shell == "cmd":
                # Use Wine for CMD emulation
                docker_command.extend([
                    "alpine:latest",
                    "sh", "-c",
                ])
                command = [" ".join(command)]  # Wrap for sh -c
            else:
                # Use Alpine Linux for bash/sh commands
                docker_command.extend([
                    "alpine:latest",
                    "sh", "-c",
                ])
                command = [" ".join(command)]  # Wrap for sh -c
            
            # Add the actual command
            docker_command.extend(command)
            
            result = subprocess.run(
                docker_command,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
            
            return result.stdout, result.stderr, result.returncode
            
        except subprocess.TimeoutExpired:
            raise HostExecutionError(f"Command timed out after {timeout}s")
        except Exception as e:
            raise HostExecutionError(f"Failed to execute via Docker: {e}")
    
    def _execute_via_ssh(
        self,
        command: List[str],
        timeout: int,
        shell: str,
    ) -> Tuple[str, str, int]:
        """Execute command on host via SSH."""
        logger.info("Executing command via SSH: %s", " ".join(command))
        
        try:
            # Build SSH command
            ssh_command = [
                "ssh",
                "-i", self.ssh_key_path,
                "-p", str(self.ssh_port),
                "-o", "StrictHostKeyChecking=no",
                "-o", "UserKnownHostsFile=/dev/null",
                "-o", f"ConnectTimeout={min(timeout, 30)}",
                f"{self.ssh_user}@{self.ssh_host}",
            ]
            
            # Add shell-specific wrapper
            if shell == "powershell":
                ssh_command.append(f"pwsh -Command '{' '.join(command)}'")
            elif shell == "cmd":
                ssh_command.append(f"cmd /c {' '.join(command)}")
            else:
                ssh_command.append(" ".join(command))
            
            result = subprocess.run(
                ssh_command,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
            
            return result.stdout, result.stderr, result.returncode
            
        except subprocess.TimeoutExpired:
            raise HostExecutionError(f"SSH command timed out after {timeout}s")
        except Exception as e:
            raise HostExecutionError(f"Failed to execute via SSH: {e}")
    
    def execute_powershell(
        self,
        command: str,
        timeout: Optional[int] = None,
    ) -> Tuple[str, str, int]:
        """Execute a PowerShell command on Windows host."""
        return self.execute([command], timeout=timeout, shell="powershell")
    
    def execute_cmd(
        self,
        command: str,
        timeout: Optional[int] = None,
    ) -> Tuple[str, str, int]:
        """Execute a CMD command on Windows host."""
        return self.execute([command], timeout=timeout, shell="cmd")
    
    def execute_bash(
        self,
        command: List[str],
        timeout: Optional[int] = None,
    ) -> Tuple[str, str, int]:
        """Execute a bash command on Linux/macOS/WSL host."""
        return self.execute(command, timeout=timeout, shell="bash")
    
    def check_host_tool(self, tool_name: str) -> bool:
        """
        Check if a CLI tool is available on the host.
        
        Args:
            tool_name: Name of the tool to check (e.g., 'npm', 'pip', 'gemini-cli')
            
        Returns:
            True if tool is available, False otherwise
        """
        try:
            stdout, stderr, returncode = self.execute(
                ["which", tool_name],
                timeout=10,
                shell="bash",
            )
            return returncode == 0
        except HostExecutionError:
            return False
    
    def invoke_cli_tool(
        self,
        tool_name: str,
        args: List[str],
        timeout: Optional[int] = None,
    ) -> Tuple[str, str, int]:
        """
        Invoke a CLI tool on the host system.
        
        This can be used to invoke tools like:
        - gemini-cli
        - claude (Anthropic CLI)
        - codex (OpenAI Codex)
        - aider
        - etc.
        
        Args:
            tool_name: Name of the CLI tool
            args: Arguments to pass to the tool
            timeout: Timeout in seconds
            
        Returns:
            Tuple of (stdout, stderr, return_code)
        """
        if not os.getenv("ENABLE_CLI_TOOLS", "true").lower() == "true":
            raise HostExecutionError("CLI tools invocation is disabled")
        
        logger.info("Invoking CLI tool on host: %s %s", tool_name, " ".join(args))
        
        # Check if tool exists first
        if not self.check_host_tool(tool_name):
            raise HostExecutionError(f"CLI tool not found on host: {tool_name}")
        
        # Execute the tool with its arguments
        command = [tool_name] + args
        return self.execute(command, timeout=timeout, shell="bash")


# Global instance
_host_executor: Optional[HostCommandExecutor] = None


def get_host_executor() -> HostCommandExecutor:
    """Get the global host executor instance."""
    global _host_executor
    if _host_executor is None:
        _host_executor = HostCommandExecutor()
    return _host_executor
