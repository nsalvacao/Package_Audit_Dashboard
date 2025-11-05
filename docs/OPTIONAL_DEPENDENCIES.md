# Optional Dependencies Guide

## Overview

Package Audit Dashboard Phase 2 features require some optional external tools. This guide explains which tools are needed and how to install them.

## Quick Reference

| Feature | Tool Required | Package Manager | Status |
|---------|--------------|-----------------|--------|
| Vulnerability Scanning (pip) | pip-audit | pip | **Recommended** |
| Dependency Trees (pip) | pipdeptree | pip | **Recommended** |
| Vulnerability Scanning (npm) | npm audit | npm | Built-in ✅ |
| Dependency Trees (npm) | npm list | npm | Built-in ✅ |

## Installation Instructions

### For Python (pip) Features

#### 1. pip-audit (Vulnerability Scanning)

**What it does:** Scans your Python packages for known security vulnerabilities

**Installation:**
```bash
pip install pip-audit
```

**Verify installation:**
```bash
pip-audit --version
# Should output: pip-audit X.X.X
```

**Test it:**
```bash
pip-audit
# Scans your current environment
```

**Without pip-audit:**
- Vulnerability scanning for pip will return: "pip-audit not installed"
- Feature gracefully degrades - no errors, just limited functionality

---

#### 2. pipdeptree (Dependency Trees)

**What it does:** Visualizes package dependency hierarchies

**Installation:**
```bash
pip install pipdeptree
```

**Verify installation:**
```bash
pipdeptree --version
# Should output: pipdeptree X.X.X
```

**Test it:**
```bash
pipdeptree
# Shows dependency tree for current environment
```

**Without pipdeptree:**
- Dependency tree will use fallback: `pip show` (less detailed)
- Still functional but with limited information

---

### For Node.js (npm) Features

#### npm audit (Vulnerability Scanning) ✅ Built-in

**Already included with npm** - No installation needed!

**Test it:**
```bash
npm audit --version
# Part of npm, no separate version
```

---

#### npm list (Dependency Trees) ✅ Built-in

**Already included with npm** - No installation needed!

**Test it:**
```bash
npm list --version
# Part of npm, no separate version
```

---

## Installation Scripts

### Install All Optional Dependencies (Recommended)

```bash
# Python tools
pip install pip-audit pipdeptree

# Verify
pip-audit --version
pipdeptree --version
```

### Install in Virtual Environment

If you're using a virtual environment for the backend:

```bash
# Activate your venv
cd backend
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install tools
pip install pip-audit pipdeptree

# These tools will only be available in this venv
```

### Global Installation

To make tools available system-wide:

```bash
# Linux/macOS
sudo pip install pip-audit pipdeptree

# Windows (run as Administrator)
pip install pip-audit pipdeptree
```

## Troubleshooting

### Issue: "pip-audit: command not found"

**Cause:** Tool not installed or not in PATH

**Solutions:**

1. **Install the tool:**
   ```bash
   pip install pip-audit
   ```

2. **Check if installed but not in PATH:**
   ```bash
   python -m pip_audit --version
   # Use 'python -m' prefix if binary not found
   ```

3. **Reinstall with --user flag:**
   ```bash
   pip install --user pip-audit
   ```

---

### Issue: "pipdeptree: command not found"

**Cause:** Tool not installed or not in PATH

**Solutions:**

1. **Install the tool:**
   ```bash
   pip install pipdeptree
   ```

2. **Use module syntax:**
   ```bash
   python -m pipdeptree
   ```

---

### Issue: "Permission denied" during installation

**Cause:** Trying to install globally without permissions

**Solutions:**

1. **Use virtual environment (recommended):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install pip-audit pipdeptree
   ```

2. **Install for current user only:**
   ```bash
   pip install --user pip-audit pipdeptree
   ```

3. **Use sudo (Linux/macOS):**
   ```bash
   sudo pip install pip-audit pipdeptree
   ```

---

### Issue: "Tool installed but API doesn't detect it"

**Cause:** Tool installed in different Python environment than backend

**Solutions:**

1. **Install in the same environment as backend:**
   ```bash
   # Activate backend's venv
   cd backend
   source .venv/bin/activate

   # Install tools
   pip install pip-audit pipdeptree

   # Restart backend
   uvicorn app.main:app --reload
   ```

2. **Check which Python the backend uses:**
   ```bash
   # From backend directory
   which python
   # Install tools using that Python
   ```

## Feature Availability Matrix

### With All Tools Installed ✅

| Feature | npm | pip | brew | winget |
|---------|-----|-----|------|--------|
| List Packages | ✅ | ✅ | ✅ | ✅ |
| Uninstall | ✅ | ✅ | ✅ | ✅ |
| Vulnerability Scan | ✅ | ✅ | ❌ | ❌ |
| Dependency Tree | ✅ | ✅ | ❌ | ❌ |
| Lockfile Export | ✅ | ✅ | ❌ | ❌ |
| Batch Operations | ✅ | ✅ | ✅ | ✅ |
| Snapshots | ✅ | ✅ | ✅ | ✅ |

### Without Optional Tools ⚠️

| Feature | npm | pip | brew | winget |
|---------|-----|-----|------|--------|
| List Packages | ✅ | ✅ | ✅ | ✅ |
| Uninstall | ✅ | ✅ | ✅ | ✅ |
| Vulnerability Scan | ✅ | ⚠️ Limited | ❌ | ❌ |
| Dependency Tree | ✅ | ⚠️ Limited | ❌ | ❌ |
| Lockfile Export | ✅ | ✅ | ❌ | ❌ |
| Batch Operations | ✅ | ✅ | ✅ | ✅ |
| Snapshots | ✅ | ✅ | ✅ | ✅ |

**Legend:**
- ✅ Fully functional
- ⚠️ Limited functionality (fallback mode)
- ❌ Not supported by package manager

## Testing Your Setup

### Quick Test Script

Save this as `test_optional_tools.py`:

```python
#!/usr/bin/env python3
import subprocess
import sys

def test_tool(name, command):
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ {name}: Installed")
            return True
        else:
            print(f"❌ {name}: Not working properly")
            return False
    except FileNotFoundError:
        print(f"❌ {name}: Not found")
        return False
    except Exception as e:
        print(f"⚠️  {name}: Error - {e}")
        return False

print("Testing Optional Dependencies...\n")

results = {
    "pip-audit": test_tool("pip-audit", ["pip-audit", "--version"]),
    "pipdeptree": test_tool("pipdeptree", ["pipdeptree", "--version"]),
    "npm": test_tool("npm", ["npm", "--version"]),
}

print("\n" + "="*50)
installed = sum(results.values())
total = len(results)
print(f"Result: {installed}/{total} tools available")

if results["npm"]:
    print("\n📦 npm features: Fully functional (built-in tools)")
else:
    print("\n⚠️  npm not found - npm features unavailable")

if results["pip-audit"] and results["pipdeptree"]:
    print("🐍 pip features: Fully functional (all tools installed)")
elif results["pip-audit"] or results["pipdeptree"]:
    print("🐍 pip features: Partially functional (some tools missing)")
else:
    print("🐍 pip features: Limited (using fallback methods)")

sys.exit(0 if installed == total else 1)
```

Run it:
```bash
python3 test_optional_tools.py
```

## Docker Users

If using Docker, add these to your `requirements.txt` or install in Dockerfile:

```dockerfile
# Dockerfile
FROM python:3.11

# ... existing setup ...

# Install optional tools
RUN pip install pip-audit pipdeptree

# ... rest of dockerfile ...
```

Or in `requirements.txt`:
```txt
# requirements.txt

# ... existing dependencies ...

# Optional tools (Phase 2 features)
pip-audit>=2.6.0
pipdeptree>=2.13.0
```

## Recommendations

### For Development
```bash
# Install everything for full feature set
pip install pip-audit pipdeptree
```

### For Production
```bash
# Install based on your needs:

# Security-focused (vulnerability scanning)
pip install pip-audit

# Dependency analysis
pip install pipdeptree

# Both (recommended)
pip install pip-audit pipdeptree
```

### For CI/CD
```bash
# Include in CI environment for testing
pip install pip-audit pipdeptree
# Then run tests to verify features work
```

## Next Steps

After installing optional dependencies:

1. ✅ Restart the backend server
2. ✅ Test vulnerability scanning via API or Dashboard
3. ✅ Test dependency trees via API or Dashboard
4. ✅ Run the test script above to verify
5. ✅ Check logs for any warnings about missing tools

## Support

If you have issues with optional dependencies:
- Check this guide's [Troubleshooting](#troubleshooting) section
- Review backend logs: Look for "pip-audit not found" messages
- Open an issue: https://github.com/nsalvacao/Package_Audit_Dashboard/issues

## Further Reading

- pip-audit documentation: https://pypi.org/project/pip-audit/
- pipdeptree documentation: https://pypi.org/project/pipdeptree/
- npm audit documentation: https://docs.npmjs.com/cli/v9/commands/npm-audit
