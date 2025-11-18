# 🚀 GitHub Codespaces Guide

Complete guide for developing Package Audit Dashboard using GitHub Codespaces.

---

## 📋 Table of Contents

1. [What is GitHub Codespaces?](#what-is-github-codespaces)
2. [Getting Started](#getting-started)
3. [First-Time Setup](#first-time-setup)
4. [Development Workflow](#development-workflow)
5. [Using GitHub Copilot](#using-github-copilot)
6. [Port Forwarding & Access](#port-forwarding--access)
7. [Running Tests](#running-tests)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)
10. [Resource Management](#resource-management)

---

## What is GitHub Codespaces?

GitHub Codespaces provides a complete, cloud-based development environment that runs in your browser or VS Code. It's like having a powerful development machine that's:

- **Instantly available** - No local setup required
- **Consistent** - Same environment for all developers
- **Powerful** - 2-32 cores, up to 64 GB RAM
- **Accessible anywhere** - Works on any device with a browser

### Your Student Developer Pack Includes:
- ✅ **180 core-hours/month** (e.g., 90 hours on 2-core or 60 hours on 4-core)
- ✅ **20 GB storage**
- ✅ **All VS Code extensions** including GitHub Copilot
- ✅ **Pre-configured environment** for this project

---

## Getting Started

### Option 1: From GitHub.com (Recommended for First Time)

1. **Navigate to the repository**: https://github.com/nsalvacao/Package_Audit_Dashboard

2. **Create Codespace**:
   - Click the green **"Code"** button
   - Select the **"Codespaces"** tab
   - Click **"Create codespace on main"** (or your branch)

   ![Create Codespace](https://docs.github.com/assets/cb-77061/mw-1440/images/help/codespaces/new-codespace-button.webp)

3. **Wait for setup** (2-5 minutes first time):
   - Container builds automatically
   - Dependencies install via post-create script
   - VS Code opens in browser

4. **Verify installation**:
   ```bash
   # Check backend
   cd backend && source .venv/bin/activate
   python -c "import fastapi; print('✓ Backend ready')"

   # Check frontend
   cd ../frontend && ls node_modules | head
   echo "✓ Frontend ready"
   ```

### Option 2: From VS Code Desktop

1. **Install VS Code Extension**:
   - Install [GitHub Codespaces extension](https://marketplace.visualstudio.com/items?itemName=GitHub.codespaces)

2. **Connect**:
   - `Cmd/Ctrl + Shift + P` → "Codespaces: Create New Codespace"
   - Select this repository
   - Choose branch
   - Select machine type (2-core recommended for development)

3. **Open**:
   - Your local VS Code connects to the cloud container
   - Full IDE features available locally

### Option 3: Quick Command Line

```bash
# Using GitHub CLI
gh codespace create -r nsalvacao/Package_Audit_Dashboard

# List your codespaces
gh codespace list

# Connect to a codespace
gh codespace ssh
```

---

## First-Time Setup

### Automatic Setup (Recommended)

The `.devcontainer/setup.sh` script runs automatically and:

✅ Creates Python virtual environment
✅ Installs all backend dependencies
✅ Installs all frontend dependencies
✅ Sets up CLI tool
✅ Creates `.env` files
✅ Configures git hooks
✅ Creates convenience scripts

### Manual Verification

After Codespace creation, verify:

```bash
# 1. Check backend
cd backend
source .venv/bin/activate
pytest tests/ -v
# Should show passing tests

# 2. Check frontend
cd ../frontend
npm run build
# Should build successfully

# 3. Check CLI
cd ../backend
python -m cli.audit_cli --help
# Should show CLI help
```

### Environment Variables

The setup automatically creates `.env` files, but you can customize:

**Backend** (`backend/.env`):
```bash
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
CORS_ORIGINS=*  # Allows Codespaces port forwarding
LOG_LEVEL=DEBUG
DEBUG=true
```

**Frontend** (`frontend/.env`):
```bash
VITE_API_URL=http://localhost:8000
VITE_DEV_TOOLS=true
```

---

## Development Workflow

### Starting the Application

#### Quick Start (All Services)

```bash
# From workspace root
./start-all.sh
```

This script:
- Starts backend on `http://localhost:8000`
- Starts frontend on `http://localhost:5173`
- Opens API docs on `http://localhost:8000/docs`

#### Manual Start (Individual Services)

**Backend**:
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0
```

**Frontend**:
```bash
cd frontend
npm run dev
```

**CLI**:
```bash
cd backend
source .venv/bin/activate
python -m cli.audit_cli discover
```

### Accessing the Application

Codespaces automatically forwards ports. You'll see notifications:

- 🌐 **Frontend**: Click "Open in Browser" for port 5173
- 🔧 **Backend API**: Access port 8000
- 📚 **API Docs**: `http://localhost:8000/docs`

URLs are publicly accessible (with authentication) or private to you.

### Making Changes

1. **Edit code** in VS Code
2. **Save** - Auto-save is enabled (1s delay)
3. **Hot reload** automatically refreshes:
   - Backend: FastAPI reloads on save
   - Frontend: Vite HMR updates instantly

4. **See changes** in the forwarded port browser tab

### Typical Development Session

```bash
# 1. Start services
./start-all.sh

# 2. Open browser to frontend (click port 5173 notification)

# 3. Make changes to code (e.g., backend/app/routers/packages.py)

# 4. Test backend changes
cd backend
source .venv/bin/activate
pytest tests/test_packages.py -v

# 5. Test frontend changes
# Just save - Vite hot-reloads automatically

# 6. Commit changes
git add .
git commit -m "feat: add package search functionality"
git push
```

---

## Using GitHub Copilot

GitHub Copilot is your AI pair programmer, included with Student Developer Pack.

### 🚀 Quick Start with Copilot

#### 1. **Inline Suggestions** (Automatic)

As you type, Copilot suggests code:

```python
# Type a comment and Copilot suggests implementation
# Function to validate package name

# Copilot will suggest:
def validate_package_name(name: str) -> bool:
    """Validate package name format."""
    if not name or len(name) < 2:
        return False
    return re.match(r'^[a-zA-Z0-9-_.]+$', name) is not None
```

**Controls**:
- `Tab` - Accept suggestion
- `Esc` - Reject suggestion
- `Alt+]` - Next suggestion
- `Alt+[` - Previous suggestion

#### 2. **Copilot Chat** (Interactive)

Open Copilot Chat sidebar (`Ctrl+Shift+I` or click Copilot icon):

**Example conversations**:

```
You: @workspace How does the snapshot system work?

Copilot: The snapshot system in this project uses the SnapshotManager
class (backend/app/analysis/snapshot.py) to create backups before
package uninstallation...
```

```
You: How can I add a new package manager adapter?

Copilot: To add a new package manager:
1. Create a new file in backend/app/adapters/
2. Extend BaseAdapter class
3. Implement required methods...
```

```
You: /explain this function
[Select a function first]

Copilot: This function validates package names using regex...
```

#### 3. **Inline Chat** (Ctrl+I)

Quick edits without leaving your code:

```python
# Select code, press Ctrl+I, type request
# Example: "Add error handling for network timeouts"

# Before
def fetch_packages():
    response = requests.get(url)
    return response.json()

# After (Copilot adds error handling)
def fetch_packages():
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        logger.error("Request timed out")
        raise
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise
```

### 🎯 Advanced Copilot Features

#### Slash Commands in Chat

- `/explain` - Explain selected code
- `/fix` - Suggest fixes for errors
- `/tests` - Generate tests
- `/doc` - Generate documentation
- `/api` - Generate API endpoints

**Example**:
```
You: /tests
[Select a function]

Copilot generates:
```python
def test_validate_package_name():
    assert validate_package_name("valid-package") == True
    assert validate_package_name("in valid") == False
    assert validate_package_name("") == False
```

#### Context Awareness with `@`

- `@workspace` - Ask about entire codebase
- `@file` - Reference specific file
- `#file` - Include file in context

**Example**:
```
You: @workspace where is authentication implemented?

Copilot: Authentication is not currently implemented in this project.
However, you could add it to backend/app/routers/auth.py...
```

#### Copilot for Testing

```bash
# 1. Write a function
def calculate_disk_usage(packages: List[Package]) -> int:
    return sum(p.size for p in packages)

# 2. Ask Copilot: "/tests generate comprehensive tests"

# 3. Copilot generates tests in chat

# 4. Run tests
pytest tests/test_analysis.py -v

# 5. If tests fail, select error and ask: "/fix"
```

### 🔄 Iterative Development with Copilot

**Workflow Example**: Adding a new feature

```
Step 1: Planning
You: @workspace I want to add a feature to export package lists to CSV.
     Where should I implement this?

Copilot: You should:
1. Add an endpoint in backend/app/routers/packages.py
2. Create a service in backend/app/services/export.py
3. Add a button in frontend/src/components/PackageList.tsx

Step 2: Implementation
You: /api create an endpoint to export packages as CSV

Copilot: [generates FastAPI endpoint code]

Step 3: Testing
You: /tests create tests for the export endpoint

Copilot: [generates pytest tests]

Step 4: Run and iterate
$ pytest tests/test_export.py -v
# Fix errors by selecting them and using /fix

Step 5: Frontend integration
You: Add a download CSV button to PackageList component

Copilot: [generates React component code]
```

### 🎨 Copilot Best Practices

1. **Write descriptive comments** - Copilot uses them as context
2. **Use meaningful variable names** - Better suggestions
3. **Select relevant code** - Copilot understands selection context
4. **Iterate with /fix** - Don't accept first suggestion blindly
5. **Review generated code** - Copilot helps but verify logic
6. **Use @workspace** - Ask questions about your codebase
7. **Generate tests first** - TDD with Copilot

### 🚫 What Copilot Should NOT Do

- ❌ Make commits for you (you control git)
- ❌ Access production systems
- ❌ Share your code externally
- ❌ Make architectural decisions without your input

---

## Port Forwarding & Access

### Automatic Port Forwarding

Codespaces automatically forwards these ports:

| Port | Service | URL |
|------|---------|-----|
| 8000 | Backend API | `http://localhost:8000` |
| 5173 | Frontend Dashboard | `http://localhost:5173` |

### Port Visibility

**Private** (default):
- Only you can access
- Requires GitHub authentication

**Public**:
- Anyone with URL can access
- Useful for sharing demos

**Change visibility**:
1. Open "PORTS" panel in VS Code
2. Right-click port
3. Select "Port Visibility" → "Public" or "Private"

### Accessing from External Tools

Get the forwarded URL:
```bash
# In Codespace terminal
gh codespace ports
```

Use in tools like Postman:
```
https://<codespace-name>-8000.preview.app.github.dev/docs
```

---

## Running Tests

### Backend Tests

```bash
# All tests
./test-backend.sh

# Specific test file
cd backend
source .venv/bin/activate
pytest tests/test_packages.py -v

# With coverage
pytest tests/ -v --cov=app --cov-report=html

# View coverage report
# Opens: backend/htmlcov/index.html (use Live Server extension)
```

### Frontend Tests

```bash
cd frontend

# Run tests (if configured)
npm test

# Lint
npm run lint

# Build
npm run build
```

### CLI Tests

```bash
cd backend
source .venv/bin/activate

# Test CLI commands
python -m cli.audit_cli discover
python -m cli.audit_cli list npm
```

---

## Troubleshooting

### Common Issues

#### 1. **Ports not forwarding**

**Symptoms**: Can't access frontend/backend
**Solution**:
```bash
# Check if services are running
ps aux | grep uvicorn
ps aux | grep vite

# Restart services
./start-all.sh

# Check PORTS panel in VS Code
```

#### 2. **Dependencies not installed**

**Symptoms**: Import errors, module not found
**Solution**:
```bash
# Backend
cd backend
source .venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

#### 3. **Virtual environment issues**

**Symptoms**: `python: command not found`, wrong Python version
**Solution**:
```bash
# Recreate venv
cd backend
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 4. **"Permission denied" errors**

**Symptoms**: Can't install packages, write files
**Solution**:
```bash
# Check user
whoami  # Should be: vscode

# Fix permissions
sudo chown -R vscode:vscode /workspace
```

#### 5. **Codespace is slow**

**Solution**:
- Upgrade machine type (Settings → Machine type)
- Close unused services
- Clear browser cache
- Rebuild container

### Rebuilding Container

If environment is broken:

1. `Cmd/Ctrl + Shift + P`
2. Type: "Codespaces: Rebuild Container"
3. Select "Rebuild Container"
4. Wait for setup to complete

**OR from terminal**:
```bash
# From local machine
gh codespace rebuild
```

### Viewing Logs

```bash
# Backend logs
cd backend
tail -f logs/app.log

# Frontend logs
# Check terminal where `npm run dev` is running

# Codespace logs
# In VS Code: View → Output → Log (Window)
```

---

## Best Practices

### 1. **Resource Management**

```bash
# Stop services when not using
pkill -f uvicorn
pkill -f vite

# Stop Codespace when done (not delete)
# From GitHub.com: Click "Stop codespace"

# Codespaces auto-stop after 30 minutes of inactivity
```

### 2. **Commit Often**

```bash
# Codespaces can be deleted anytime
# Always push your changes

git add .
git commit -m "feat: descriptive message"
git push
```

### 3. **Use Branches**

```bash
# Create feature branch
git checkout -b feature/new-feature

# Push branch
git push -u origin feature/new-feature

# Codespace follows your branch
```

### 4. **Leverage Extensions**

Pre-installed extensions:
- **GitLens**: Enhanced git features
- **Thunder Client**: API testing (alternative to Postman)
- **Todo Tree**: Track TODOs in code
- **Error Lens**: Inline error messages

### 5. **Shortcuts**

| Shortcut | Action |
|----------|--------|
| `Ctrl + `` | Toggle terminal |
| `Ctrl + Shift + E` | Explorer |
| `Ctrl + Shift + F` | Search |
| `Ctrl + P` | Quick file open |
| `Ctrl + Shift + P` | Command palette |
| `Ctrl + I` | Copilot inline chat |

---

## Resource Management

### Understanding Your Quota

**Student Developer Pack**:
- 180 core-hours/month
- Calculation: `hours_used = runtime_hours × cores`

**Examples**:
- 2-core machine: 90 hours/month (3 hours/day)
- 4-core machine: 45 hours/month (1.5 hours/day)

### Monitoring Usage

1. **GitHub.com**:
   - Settings → Billing → Codespaces
   - View current usage

2. **VS Code**:
   - Bottom bar shows machine type
   - Hover for usage details

### Optimization Tips

1. **Right-size your machine**:
   - Development: 2-core (sufficient for this project)
   - Testing: 4-core (faster test runs)
   - Production builds: 8-core (occasional use)

2. **Stop when idle**:
   - Auto-stop is set to 30 minutes
   - Manually stop if stepping away

3. **Delete unused Codespaces**:
   - Keep max 1-2 active per project
   - Delete from GitHub.com → Codespaces

4. **Use local dev when possible**:
   - Codespaces for cloud/collaboration
   - Local machine for extended sessions

### Changing Machine Type

1. **In Codespace**:
   - `Ctrl + Shift + P`
   - "Codespaces: Change Machine Type"
   - Select new type
   - Codespace restarts

2. **Before creation**:
   - Click "..." when creating
   - Select machine type
   - Then create

---

## FAQ

**Q: Can I use Codespaces on a tablet?**
A: Yes! Works in any modern browser. iPad/Android tablet with browser.

**Q: How do I share my Codespace?**
A: Make ports public, share the URL. Or use Live Share extension for real-time collaboration.

**Q: Can I use multiple Codespaces?**
A: Yes, but each counts toward your quota. Keep only what you need.

**Q: What happens if I exceed my quota?**
A: Codespaces stop running. You can upgrade billing or wait for monthly reset.

**Q: Can I customize the devcontainer?**
A: Yes! Edit `.devcontainer/devcontainer.json`. See [devcontainers spec](https://containers.dev/).

**Q: How do I debug in Codespaces?**
A: Same as local VS Code. Use Debug panel, set breakpoints, press F5.

**Q: Can I use Docker in Codespaces?**
A: Yes! Docker-in-Docker is enabled. Run `docker ps` to verify.

**Q: Is my code secure?**
A: Yes. Codespaces are isolated containers. Private repos stay private. See [GitHub security](https://docs.github.com/en/codespaces/security).

---

## Additional Resources

- 📘 [GitHub Codespaces Documentation](https://docs.github.com/en/codespaces)
- 🎓 [Codespaces Quickstart](https://docs.github.com/en/codespaces/getting-started/quickstart)
- 🤖 [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- 🛠️ [Devcontainer Specification](https://containers.dev/)
- 💬 [GitHub Community Forum](https://github.com/orgs/community/discussions/categories/codespaces)

---

## Getting Help

1. **In Codespace**:
   - Click Copilot icon → Ask questions
   - `@workspace` for codebase questions

2. **GitHub**:
   - Create issue in this repository
   - Check existing issues first

3. **Documentation**:
   - See `docs/` folder for specific topics
   - README.md for project overview

4. **Community**:
   - GitHub Discussions
   - Stack Overflow: tag `github-codespaces`

---

**Happy Coding! 🚀**

*Last updated: 2025-11-18*
