# 🛠️ PATH Setup Guide

## Overview

This guide helps you configure your system PATH to ensure package managers are correctly detected by the Package Audit Dashboard.

---

## Quick Diagnostics

### Check Current PATH

```bash
# Unix/macOS/Linux
echo $PATH

# Windows (PowerShell)
$env:PATH

# Windows (CMD)
echo %PATH%
```

### Test Package Manager Detection

```bash
# Check if package managers are in PATH
which npm     # or: where npm (Windows)
which pip
which brew    # macOS only
which winget  # Windows only
```

---

## Common PATH Issues

### Issue 1: Package Manager Not Found

**Symptom**: Dashboard shows "No package managers detected"

**Diagnosis**:
```bash
which npm  # Returns "not found"
```

**Solution**: Add package manager directory to PATH

---

## Platform-Specific Setup

### 🐧 Linux

#### Add npm to PATH

```bash
# Find npm location
npm_path=$(which npm 2>/dev/null || echo "$HOME/.npm-global/bin")

# Add to PATH (temporary)
export PATH="$npm_path:$PATH"

# Add to PATH (permanent - Bash)
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Add to PATH (permanent - Zsh)
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### Add pip to PATH

```bash
# Python user scripts directory
export PATH="$HOME/.local/bin:$PATH"

# Add to shell config
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

### 🍎 macOS

#### Add Homebrew to PATH

```bash
# Intel Macs
echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zshrc

# Apple Silicon Macs
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc

# Apply changes
source ~/.zshrc
```

#### Add npm to PATH (via Homebrew)

```bash
# Homebrew npm
export PATH="/usr/local/opt/node/bin:$PATH"

# Or nvm (if using Node Version Manager)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

---

### 🪟 Windows

#### Add npm to PATH

1. **Find Node.js installation directory**:
   ```powershell
   Get-Command node | Select-Object -ExpandProperty Source
   # Example: C:\Program Files\nodejs\node.exe
   ```

2. **Open Environment Variables**:
   - Press `Win + X` → System → Advanced system settings
   - Click "Environment Variables"

3. **Edit PATH**:
   - Under "User variables", select `Path` → Edit
   - Add: `C:\Program Files\nodejs`
   - Click OK

4. **Restart terminal** and verify:
   ```powershell
   npm --version
   ```

#### Add WinGet to PATH

WinGet is usually pre-installed on Windows 11. If not:

1. Install from Microsoft Store: "App Installer"
2. Verify:
   ```powershell
   winget --version
   ```

If still not found:
```powershell
# Add Windows Apps path
$env:PATH += ";C:\Users\$env:USERNAME\AppData\Local\Microsoft\WindowsApps"
```

---

## Script-Based PATH Fixes

### Generate PATH Fix Script (Unix/macOS)

The dashboard can generate a custom fix script:

```bash
# Run from backend directory
python -c "from app.routers.path import generate_path_script; print(generate_path_script())"
```

This generates:
```bash
#!/bin/bash
# Auto-generated PATH fix script

export PATH="/usr/local/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/.npm-global/bin:$PATH"

echo "PATH updated. Run 'source ~/.bashrc' to apply."
```

---

## Verification

### After PATH Configuration

```bash
# Test all package managers
npm --version
pip --version
brew --version  # macOS
winget --version  # Windows

# Restart dashboard backend
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload

# Visit dashboard
open http://localhost:5173
```

Expected result: All installed package managers should now appear in the dashboard.

---

## Advanced Configuration

### Multiple Node Versions (nvm)

If using Node Version Manager:

```bash
# Add to ~/.bashrc or ~/.zshrc
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"

# Set default Node version
nvm alias default 18
```

### Multiple Python Versions (pyenv)

```bash
# Add to ~/.bashrc or ~/.zshrc
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

### Virtual Environments

The dashboard respects active virtual environments:

```bash
# Activate Python venv
source .venv/bin/activate

# Dashboard will detect pip from active venv
pip --version  # Shows venv pip
```

---

## Troubleshooting

### Problem: PATH Changes Don't Persist

**Cause**: Added to wrong shell config file

**Solution**:
```bash
# Check your shell
echo $SHELL

# Bash users: ~/.bashrc
# Zsh users: ~/.zshrc
# Fish users: ~/.config/fish/config.fish
```

---

### Problem: Permission Denied

**Cause**: Trying to modify system PATH without sudo

**Solution**: Use user-level PATH modifications only
```bash
# ✅ Good (user-level)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# ❌ Bad (requires sudo)
echo 'export PATH="/usr/local/bin:$PATH"' >> /etc/environment
```

---

### Problem: Dashboard Still Doesn't Detect Managers

**Diagnosis**:
1. Verify PATH in current shell:
   ```bash
   echo $PATH | tr ':' '\n'  # Unix
   ```

2. Verify package manager works:
   ```bash
   which npm && npm --version
   ```

3. Restart backend server:
   ```bash
   # Backend must be restarted after PATH changes
   cd backend
   source .venv/bin/activate
   uvicorn app.main:app --reload
   ```

4. Check backend logs:
   ```bash
   tail -f ~/.package-audit/logs/operations.log
   ```

---

## Environment Variables Reference

### Required

| Variable | Purpose | Example |
|----------|---------|---------|
| `PATH` | Executable search paths | `/usr/local/bin:/usr/bin` |

### Optional (Version Managers)

| Variable | Purpose | Example |
|----------|---------|---------|
| `NVM_DIR` | Node Version Manager | `$HOME/.nvm` |
| `PYENV_ROOT` | Python Version Manager | `$HOME/.pyenv` |
| `CARGO_HOME` | Rust package manager | `$HOME/.cargo` |

---

## Shell Configuration Files

### Bash
- **Interactive login**: `~/.bash_profile`, `~/.bash_login`, `~/.profile`
- **Interactive non-login**: `~/.bashrc`
- **Recommended**: Add to `~/.bashrc`

### Zsh
- **Interactive**: `~/.zshrc`
- **Login**: `~/.zprofile`
- **Recommended**: Add to `~/.zshrc`

### Fish
- **Interactive**: `~/.config/fish/config.fish`

---

## Additional Resources

- [Node.js PATH setup](https://nodejs.org/en/download/package-manager/)
- [Python PATH setup](https://docs.python.org/3/using/cmdline.html#envvar-PATH)
- [Homebrew PATH setup](https://docs.brew.sh/FAQ#my-mac-apps-dont-find-homebrew-utilities)
- [WinGet setup](https://learn.microsoft.com/en-us/windows/package-manager/winget/)

---

**Last Updated**: 2025-11-05
**Compatibility**: Linux, macOS, Windows
