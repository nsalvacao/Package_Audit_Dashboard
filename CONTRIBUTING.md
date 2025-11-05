# Contributing to Package Audit Dashboard

First off, thank you for considering contributing to Package Audit Dashboard! It's people like you that make this tool better for everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Guidelines](#coding-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please be respectful and constructive in all interactions.

### Our Standards

- **Be Respectful**: Treat everyone with respect and kindness
- **Be Collaborative**: Work together towards common goals
- **Be Professional**: Maintain professional conduct
- **Be Inclusive**: Welcome and support people of all backgrounds

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+
- Git
- Docker (optional, for containerized development)

### Finding Issues to Work On

- Check the [Issues page](https://github.com/nsalvacao/Package_Audit_Dashboard/issues)
- Look for labels:
  - `good first issue` - Great for newcomers
  - `help wanted` - We need assistance with these
  - `bug` - Something isn't working
  - `enhancement` - New feature or request

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/Package_Audit_Dashboard.git
cd Package_Audit_Dashboard

# Add upstream remote
git remote add upstream https://github.com/nsalvacao/Package_Audit_Dashboard.git
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov pytest-asyncio black flake8 mypy

# Install optional tools (for Phase 2 features)
pip install pip-audit pipdeptree

# Run tests to verify setup
pytest tests/ -v
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run linter
npm run lint

# Start development server
npm run dev
```

### 4. Using Docker (Alternative)

```bash
# Start all services
docker-compose up

# Run tests
docker-compose exec backend pytest tests/ -v
docker-compose exec frontend npm run lint
```

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check if the issue already exists. When creating a bug report, include:

- **Clear title** - Describe the bug in one sentence
- **Description** - Detailed explanation of the bug
- **Steps to Reproduce** - How to trigger the bug
- **Expected Behavior** - What should happen
- **Actual Behavior** - What actually happens
- **Environment** - OS, Python version, Node version, etc.
- **Screenshots** - If applicable

**Bug Report Template:**

```markdown
### Description
Brief description of the bug

### Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

### Expected Behavior
What should happen

### Actual Behavior
What actually happens

### Environment
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.11.4]
- Node: [e.g., 18.16.0]
- Browser: [e.g., Chrome 114]
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title** - Describe the enhancement
- **Use Case** - Why is this needed?
- **Proposed Solution** - How would it work?
- **Alternatives** - Other solutions you've considered
- **Additional Context** - Screenshots, mockups, etc.

### Code Contributions

1. **Check existing issues** - Make sure nobody else is working on it
2. **Create an issue** - Discuss your approach before coding
3. **Fork the repository** - Work on your own fork
4. **Create a branch** - Use a descriptive name
5. **Make your changes** - Follow coding guidelines
6. **Test thoroughly** - Add/update tests
7. **Update documentation** - If needed
8. **Submit a PR** - Follow the PR template

## Coding Guidelines

### Python (Backend)

#### Style Guide

- Follow **PEP 8** style guide
- Use **Black** for code formatting
- Maximum line length: 120 characters
- Use type hints where possible

```python
# Good
def get_packages(manager_id: str, force: bool = False) -> list[Package]:
    """Get all packages for a manager."""
    pass

# Avoid
def get_packages(manager_id, force=False):
    pass
```

#### Code Formatting

```bash
# Format code with Black
black app/ tests/

# Check with Flake8
flake8 app/ tests/ --max-line-length=120

# Type checking with MyPy
mypy app/ --ignore-missing-imports
```

#### Best Practices

- **Functions**: Keep them small and focused
- **Docstrings**: Use Google-style docstrings
- **Error Handling**: Always catch specific exceptions
- **Type Hints**: Use for function signatures
- **Async/Await**: Use for I/O operations

**Example:**

```python
async def uninstall_package(
    manager_id: str,
    package_name: str,
    force: bool = False
) -> UninstallResult:
    """
    Uninstall a package from a package manager.

    Args:
        manager_id: ID of the package manager (npm, pip, etc.)
        package_name: Name of the package to uninstall
        force: Skip confirmation prompts

    Returns:
        UninstallResult with status and details

    Raises:
        ValidationError: If package_name is invalid
        ManagerNotFoundError: If manager_id doesn't exist
    """
    # Implementation
    pass
```

### TypeScript/React (Frontend)

#### Style Guide

- Use **TypeScript** for all new code
- Follow **ESLint** configuration
- Use **functional components** with hooks
- Prefer **named exports**

```typescript
// Good
export function Dashboard(): JSX.Element {
  const [data, setData] = useState<Manager[]>([])
  // ...
}

// Avoid
export default () => {
  const [data, setData] = useState([])
  // ...
}
```

#### Component Structure

```typescript
import { useState } from 'react'

interface ComponentProps {
  title: string
  onAction?: () => void
}

export function Component({ title, onAction }: ComponentProps): JSX.Element {
  const [state, setState] = useState<string>('')

  const handleClick = () => {
    // Handler logic
    onAction?.()
  }

  return (
    <div>
      {/* Component JSX */}
    </div>
  )
}
```

#### Best Practices

- **Props**: Always define interfaces
- **State**: Use TypeScript generics
- **Effects**: Keep them focused and clean up
- **Queries**: Use React Query for data fetching
- **Styling**: Use Tailwind CSS utility classes

### Git Workflow

#### Branch Naming

```bash
# Feature branches
git checkout -b feature/add-vulnerability-scan

# Bug fixes
git checkout -b fix/package-list-crash

# Documentation
git checkout -b docs/update-api-guide

# Refactoring
git checkout -b refactor/simplify-validation
```

#### Keeping Your Fork Updated

```bash
# Fetch upstream changes
git fetch upstream

# Merge into your main branch
git checkout main
git merge upstream/main

# Rebase your feature branch
git checkout feature/your-feature
git rebase main
```

## Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

### Examples

```bash
# Feature
feat(backend): add health check endpoint

Add /health endpoint for monitoring and load balancers.
Includes basic status and detailed system information.

# Bug fix
fix(frontend): resolve vulnerability scan infinite loop

Fixed issue where vulnerability scan would loop indefinitely
when pip-audit returned empty results.

Closes #123

# Documentation
docs: update Docker setup guide

Add troubleshooting section for common Docker issues.
Include examples for multi-stage builds.

# Breaking change
feat(api)!: change snapshot API response format

BREAKING CHANGE: Snapshot API now returns ISO timestamps
instead of Unix timestamps. Update clients accordingly.
```

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass locally
- [ ] No new warnings introduced

### PR Checklist

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests**
   ```bash
   # Backend
   cd backend
   pytest tests/ -v

   # Frontend
   cd frontend
   npm run lint
   npm run build
   ```

3. **Create PR**
   - Use the PR template
   - Link related issues
   - Add screenshots if UI changes
   - Request review from maintainers

### PR Review Process

1. **Automated Checks** - CI/CD must pass
2. **Code Review** - At least one approval required
3. **Testing** - Verify changes work as expected
4. **Merge** - Maintainer will merge when approved

### After PR is Merged

```bash
# Update your local main
git checkout main
git pull upstream main

# Delete feature branch
git branch -d feature/your-feature
git push origin --delete feature/your-feature
```

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_validation.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Writing Tests

```python
import pytest
from app.core.validation import ValidationLayer

def test_validate_package_name_valid():
    """Test validation of valid package names."""
    validator = ValidationLayer()

    # Should not raise
    validator.validate_package_name("express")
    validator.validate_package_name("@types/node")
    validator.validate_package_name("lodash-es")

def test_validate_package_name_invalid():
    """Test validation rejects invalid package names."""
    validator = ValidationLayer()

    # Should raise ValidationError
    with pytest.raises(ValidationError):
        validator.validate_package_name("../../../etc/passwd")
```

### Frontend Tests

```bash
cd frontend

# Run linter
npm run lint

# Fix linting issues
npm run lint -- --fix

# Build (catches TypeScript errors)
npm run build
```

## Documentation

### Code Documentation

- **Python**: Use docstrings (Google style)
- **TypeScript**: Use JSDoc comments
- **Markdown**: For user-facing documentation

### Documentation Files

Update relevant documentation:
- **README.md** - Main project documentation
- **API.md** - API endpoint documentation
- **SECURITY.md** - Security-related documentation
- **docs/*.md** - Specific feature documentation

### API Documentation

FastAPI generates automatic documentation. Update docstrings:

```python
@router.get("/packages")
async def list_packages(
    manager_id: str,
    limit: int = 100
) -> PackageList:
    """
    List all packages for a package manager.

    Args:
        manager_id: Package manager identifier (npm, pip, etc.)
        limit: Maximum number of packages to return

    Returns:
        List of packages with metadata

    Raises:
        HTTPException: 404 if manager not found
    """
    pass
```

## Questions?

- **General Questions**: Open a [Discussion](https://github.com/nsalvacao/Package_Audit_Dashboard/discussions)
- **Bug Reports**: Open an [Issue](https://github.com/nsalvacao/Package_Audit_Dashboard/issues)
- **Security Issues**: See [SECURITY.md](SECURITY.md)

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
