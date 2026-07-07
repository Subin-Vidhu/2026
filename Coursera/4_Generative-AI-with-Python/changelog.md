# Changelog

This file records setup issues, fixes, and the exact commands used in this folder so the next time something breaks, the recovery path is already documented.

## 2026-07-07

### What was fixed

- Converted the folder from a plain `requirements.txt` setup into a `uv` project by adding `pyproject.toml`.
- Recreated the environment with Python 3.13.
- Changed the project to dependency-only mode so `uv sync` would not try to build this course repository as a Python package.
- Added `.python-version` so future `uv` commands default to Python 3.13.

### Issues encountered

1. `uv sync` failed at first because there was no `pyproject.toml`.
2. `uv deactivate` does not exist.
3. The old fully pinned dependency set did not resolve cleanly on Python 3.13.
4. `uv` then tried to build the repo as an editable package, but this folder is not a package and does not contain a module like `src/generative_ai_with_python/__init__.py`.

### Commands used

#### Check available Python versions

```powershell
py -0p
```

#### Create or refresh the uv environment with Python 3.13

```powershell
Set-Location 'd:\2026\Coursera\4_Generative-AI-with-Python'
uv sync --python 3.13
```

#### Verify that the virtual environment was created

```powershell
Set-Location 'd:\2026\Coursera\4_Generative-AI-with-Python'
if (Test-Path .venv) { Get-ChildItem -Force .venv | Select-Object -First 5 } else { 'NO_VENV_YET' }
```

### Terminal activation and deactivation

#### Activate the virtual environment on Windows PowerShell

```powershell
Set-Location 'd:\2026\Coursera\4_Generative-AI-with-Python'
.\.venv\Scripts\Activate.ps1
```

#### Activate the virtual environment on Windows Command Prompt

```bat
cd /d d:\2026\Coursera\4_Generative-AI-with-Python
.venv\Scripts\activate.bat
```

#### Deactivate the virtual environment

```powershell
deactivate
```

If Conda is also active, run:

```powershell
conda deactivate
```

### What to do if `uv sync` fails again

1. Check that `pyproject.toml` exists in the current folder.
2. Confirm the intended Python version with `py -0p`.
3. Run `uv sync --python 3.13` from this folder.
4. If dependency resolution fails, compare `requirements.txt` and `requirementsMAC.txt` for overly strict pins.
5. If `uv` complains about building a package, ensure the project is marked as dependency-only with `package = false` in `[tool.uv]`.
6. If the environment seems stale, remove `.venv` and rerun `uv sync --python 3.13`.

### Maintenance rule

Any future change in this folder should update this changelog with:

- what changed,
- why it changed,
- the exact command used,
- and any new failure or recovery step discovered.
