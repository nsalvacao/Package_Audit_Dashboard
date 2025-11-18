# Codespaces development container
FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

# Install Node.js (handled by feature, but ensuring dependencies)
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    curl \
    wget \
    git \
    build-essential \
    vim \
    nano \
    zsh \
    # Python build dependencies
    python3-dev \
    python3-pip \
    python3-venv \
    # For package manager testing
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    software-properties-common \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /workspace

# Install global Python tools
RUN pip install --upgrade pip setuptools wheel \
    && pip install black flake8 mypy pytest pytest-cov ipython

# Install global Node tools (will be available after Node feature installs)
# These will be installed in post-create script

# Configure git for better UX
RUN git config --global --add safe.directory /workspace

# Set default shell to zsh
ENV SHELL=/bin/zsh

# Create vscode user's directories
RUN mkdir -p /home/vscode/.vscode-server/extensions \
    && mkdir -p /home/vscode/.vscode-server-insiders/extensions \
    && chown -R vscode:vscode /home/vscode/.vscode-server \
    && chown -R vscode:vscode /home/vscode/.vscode-server-insiders

# Switch to vscode user
USER vscode

# Configure Zsh with oh-my-zsh plugins
RUN echo 'export WORKSPACE_DIR=/workspace' >> ~/.zshrc \
    && echo 'export PYTHONPATH=/workspace/backend:$PYTHONPATH' >> ~/.zshrc \
    && echo 'export PATH=/workspace/backend/.venv/bin:$PATH' >> ~/.zshrc \
    && echo 'alias ll="ls -lah"' >> ~/.zshrc \
    && echo 'alias be="cd /workspace/backend"' >> ~/.zshrc \
    && echo 'alias fe="cd /workspace/frontend"' >> ~/.zshrc \
    && echo 'alias serve-backend="cd /workspace/backend && source .venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0"' >> ~/.zshrc \
    && echo 'alias serve-frontend="cd /workspace/frontend && npm run dev"' >> ~/.zshrc \
    && echo 'alias test-backend="cd /workspace/backend && source .venv/bin/activate && pytest tests/ -v"' >> ~/.zshrc

CMD ["sleep", "infinity"]
