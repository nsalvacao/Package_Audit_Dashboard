## 📋 Tabela de comandos úteis por gestor

|Gestor|Listar pacotes/versões|Instalar|Atualizar|Remover/Desinstalar|Outros úteis|
|---|---|---|---|---|---|
|**npm**|`npm list -g --depth=0`|`npm install -g <pkg>`|`npm update -g <pkg>` ou `npm update -g`|`npm uninstall -g <pkg>`|`npm outdated -g` (ver updates disponíveis)|
|**pnpm**|`pnpm list -g --depth=0`|`pnpm add -g <pkg>`|`pnpm update -g <pkg>`|`pnpm remove -g <pkg>`|`pnpm outdated -g`|
|**pip**|`pip list`|`pip install <pkg>`|`pip install --upgrade <pkg>`|`pip uninstall <pkg>`|`pip freeze > requirements.txt` (snapshot)|
|**pipx**|`pipx list`|`pipx install <pkg>`|`pipx upgrade <pkg>` ou `pipx upgrade-all`|`pipx uninstall <pkg>`|`pipx reinstall-all` (útil após upgrade do Python)|
|**winget**|`winget list`|`winget install <pkg>`|`winget upgrade <pkg>` ou `winget upgrade --all`|`winget uninstall <pkg>`|`winget search <nome>`|
|**nvm (Windows/Linux)**|`nvm list`|`nvm install <versão>`|`nvm install <versão> --reinstall-packages-from=current`|`nvm uninstall <versão>`|`nvm use <versão>` (trocar runtime)|
|**choco**|`choco list -l`|`choco install <pkg>`|`choco upgrade <pkg>` ou `choco upgrade all`|`choco uninstall <pkg>`|`choco outdated`|
|**uv** (Python)|`uv pip list`|`uv pip install <pkg>`|`uv pip install --upgrade <pkg>`|`uv pip uninstall <pkg>`|`uv venv` (criar ambiente), `uv sync` (sincronizar deps)|

---

## 📋 Tabela de comandos úteis para auditoria/manutenção

|Gestor|Comando de ajuda|Auditoria / Diagnóstico|Outros comandos úteis de manutenção|
|---|---|---|---|
|**npm**|`npm help` ou `npm help <cmd>`|`npm audit` (verifica vulnerabilidades), `npm audit fix` (corrige) [npm Docs](https://docs.npmjs.com/cli/v10/commands/npm-audit/?v=true)|`npm outdated` (pacotes desatualizados), `npm doctor` (diagnóstico do ambiente)|
|**pnpm**|`pnpm help` ou `pnpm <cmd> --help` [pnpm](https://pnpm.io/pt/pnpm-cli)|`pnpm audit` (auditoria de segurança), `pnpm outdated` (pacotes desatualizados)|`pnpm why <pkg>` (explica dependência), `pnpm store status` (estado do cache)|
|**pip**|`pip help` ou `pip <cmd> --help` [pip](https://pip.pypa.io/en/stable/cli/index.html)|`pip check` (verifica dependências quebradas), `pip debug` (info do ambiente)|`pip show <pkg>` (detalhes de pacote), `pip cache info` (estado do cache)|
|**pipx**|`pipx --help` ou `pipx <cmd> --help` [pipx.pypa.io](https://pipx.pypa.io/latest/docs/)|`pipx list` (inventário de apps), `pipx environment` (variáveis e paths)|`pipx run <pkg>` (executa sem instalar), `pipx inject <pkg> <dep>` (injeta dependências extras)|
|**winget**|`winget --help` ou `winget <cmd> --help` [Microsoft Learn](https://learn.microsoft.com/pt-br/windows/package-manager/winget/)|`winget list` (apps instalados), `winget upgrade` (lista updates disponíveis)|`winget upgrade --all` (atualiza tudo), `winget search <nome>` (procurar apps)|
|**nvm**|`nvm --help` [GitHub Gist](https://gist.github.com/chranderson/b0a02781c232f170db634b40c97ff455)|`nvm ls` (versões instaladas), `nvm ls-remote` (versões disponíveis online)|`nvm alias default <versão>` (define padrão), `nvm which <versão>` (path do binário)|
|**choco**|`choco -?` ou `choco <cmd> -?` [Chocolatey Software](https://docs.chocolatey.org/en-us/choco/commands/)|`choco outdated` (pacotes desatualizados), `choco info <pkg>` (detalhes)|`choco pin list` (pacotes fixados), `choco config list` (config ativa), `choco feature list`|
|**uv**|`uv --help` ou `uv <cmd> --help` [DataCamp](https://www.datacamp.com/pt/tutorial/python-uv)|`uv pip check` (verifica dependências), `uv pip list` (lista pacotes)|`uv venv` (cria ambientes), `uv sync` (sincroniza dependências), `uv lock` (gera lockfile reprodutível)|

---

## 🔑 Destaques

- **npm/pnpm**: têm comandos de **auditoria de segurança** integrados (`audit`).
- **pip/pipx/uv**: oferecem comandos de **checagem de dependências** e **ambientes isolados**.
- **winget/choco**: focam em **inventário e atualização de apps de sistema**.
- **nvm**: não faz auditoria de pacotes, mas é essencial para **gestão de versões Node**.

---

## 🔑 Observações

- **npm/pnpm** → `-g` é para pacotes globais; sem `-g` atua no projeto local.
- **pip** → convém usar sempre em **venvs** (ou `uv`/`pipx`) para evitar poluição global.
- **pipx** → ideal para CLIs Python isolados.
- **winget/choco** → atuam a nível de sistema (apps Windows).
- **nvm** → não gere pacotes, apenas versões do Node.js.
- **uv** → substituto moderno do `pip`/`pip-tools`, muito mais rápido e declarativo.
