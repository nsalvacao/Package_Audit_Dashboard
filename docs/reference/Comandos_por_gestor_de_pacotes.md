## 📋 Useful Commands by Package Manager

| Manager | List packages/versions | Install | Update | Remove/Uninstall | Other useful commands |
|---------|------------------------|---------|--------|------------------|-----------------------|
| **npm** | `npm list -g --depth=0` | `npm install -g <pkg>` | `npm update -g <pkg>` or `npm update -g` | `npm uninstall -g <pkg>` | `npm outdated -g` (check for updates) |
| **pnpm** | `pnpm list -g --depth=0` | `pnpm add -g <pkg>` | `pnpm update -g <pkg>` | `pnpm remove -g <pkg>` | `pnpm outdated -g` |
| **pip** | `pip list` | `pip install <pkg>` | `pip install --upgrade <pkg>` | `pip uninstall <pkg>` | `pip freeze > requirements.txt` (snapshot) |
| **pipx** | `pipx list` | `pipx install <pkg>` | `pipx upgrade <pkg>` or `pipx upgrade-all` | `pipx uninstall <pkg>` | `pipx reinstall-all` (useful after upgrading Python) |
| **winget** | `winget list` | `winget install <pkg>` | `winget upgrade <pkg>` or `winget upgrade --all` | `winget uninstall <pkg>` | `winget search <name>` |
| **nvm (Windows/Linux)** | `nvm list` | `nvm install <version>` | `nvm install <version> --reinstall-packages-from=current` | `nvm uninstall <version>` | `nvm use <version>` (switch runtime) |
| **choco** | `choco list -l` | `choco install <pkg>` | `choco upgrade <pkg>` or `choco upgrade all` | `choco uninstall <pkg>` | `choco outdated` |
| **uv** (Python) | `uv pip list` | `uv pip install <pkg>` | `uv pip install --upgrade <pkg>` | `uv pip uninstall <pkg>` | `uv venv` (create environment), `uv sync` (sync dependencies) |

---

## 📋 Audit and Maintenance Commands

| Manager | Help command | Audit / Diagnostics | Other maintenance commands |
|---------|--------------|---------------------|----------------------------|
| **npm** | `npm help` or `npm help <cmd>` | `npm audit` (security scan), `npm audit fix` (autofix) — [npm Docs](https://docs.npmjs.com/cli/v10/commands/npm-audit/?v=true) | `npm outdated` (outdated packages), `npm doctor` (environment diagnostics) |
| **pnpm** | `pnpm help` or `pnpm <cmd> --help` — [pnpm](https://pnpm.io/pnpm-cli) | `pnpm audit` (security), `pnpm outdated` (stale packages) | `pnpm why <pkg>` (dependency graph), `pnpm store status` (cache state) |
| **pip** | `pip help` or `pip <cmd> --help` — [pip](https://pip.pypa.io/en/stable/cli/index.html) | `pip check` (broken dependencies), `pip debug` (environment info) | `pip show <pkg>` (package details), `pip cache info` (cache state) |
| **pipx** | `pipx --help` or `pipx <cmd> --help` — [pipx.pypa.io](https://pipx.pypa.io/latest/docs/) | `pipx list` (inventory), `pipx environment` (variables and paths) | `pipx run <pkg>` (run without install), `pipx inject <pkg> <dep>` (inject extra dependencies) |
| **winget** | `winget --help` or `winget <cmd> --help` — [Microsoft Learn](https://learn.microsoft.com/windows/package-manager/winget/) | `winget list` (installed apps), `winget upgrade` (available updates) | `winget upgrade --all` (upgrade everything), `winget search <name>` (find apps) |
| **nvm** | `nvm --help` — [GitHub Gist](https://gist.github.com/chranderson/b0a02781c232f170db634b40c97ff455) | `nvm ls` (installed versions), `nvm ls-remote` (remote versions) | `nvm alias default <version>` (set default), `nvm which <version>` (binary path) |
| **choco** | `choco -?` or `choco <cmd> -?` — [Chocolatey Software](https://docs.chocolatey.org/en-us/choco/commands/) | `choco outdated` (stale packages), `choco info <pkg>` (details) | `choco pin list` (pinned packages), `choco config list` (active config), `choco feature list` |
| **uv** | `uv --help` or `uv <cmd> --help` — [DataCamp](https://www.datacamp.com/tutorial/python-uv) | `uv pip check` (dependency validation), `uv pip list` (package inventory) | `uv venv` (create environments), `uv sync` (sync dependencies), `uv lock` (generate reproducible lockfile) |

---

## 🔑 Highlights

- **npm/pnpm:** include built-in **security audit** commands (`audit`).
- **pip/pipx/uv:** provide **dependency checking** and **isolated environments**.
- **winget/choco:** focus on **system-level inventory and updates**.
- **nvm:** manages **Node.js runtime versions** rather than packages.

---

## 🔑 Notes

- **npm/pnpm** — use `-g` for global packages; omit it for project-level operations.
- **pip** — prefer virtual environments (or `uv`/`pipx`) to avoid polluting the global interpreter.
- **pipx** — ideal for isolated Python CLIs.
- **winget/choco** — operate at the Windows system level.
- **nvm** — handles Node.js versions, not packages.
- **uv** — modern replacement for `pip`/`pip-tools`, faster and declarative.
