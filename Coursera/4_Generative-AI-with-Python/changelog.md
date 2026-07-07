# Changelog

This file records setup issues, fixes, and the exact commands used in this folder so the next time something breaks, the recovery path is already documented.

## 2026-07-07

### What was fixed

- Converted the folder from a plain `requirements.txt` setup into a `uv` project by adding `pyproject.toml`.
- Recreated the environment with Python 3.13.
- Changed the project to dependency-only mode so `uv sync` would not try to build this course repository as a Python package.
- Added `.python-version` so future `uv` commands default to Python 3.13.

### New issue discovered during sync

- `uv sync --python 3.13` still failed on Windows because `llama-cpp-python` tried to build from source and required `nmake` plus a C/C++ compiler toolchain.
- That package is not referenced anywhere in the course folders, so the practical fix is to skip it on Windows rather than block the whole environment.
- After skipping `llama-cpp-python`, `uv` still tried to build `numpy==1.26.4` from source on Python 3.13, which is not what we want for a clean Windows setup.

### Issues encountered

1. `uv sync` failed at first because there was no `pyproject.toml`.
2. `uv deactivate` does not exist.
3. The old fully pinned dependency set did not resolve cleanly on Python 3.13.
4. `uv` then tried to build the repo as an editable package, but this folder is not a package and does not contain a module like `src/generative_ai_with_python/__init__.py`.
5. `llama-cpp-python==0.3.33` tried to build from source but failed: CMake could not find `nmake` because native C++ build tools (Microsoft Visual C++) are not installed on Windows.
6. `numpy==1.24.1` (upper bound <1.28) tried to build from source for Python 3.13, which is slow and requires build tools.
5. `llama-cpp-python` failed to build on Windows because `nmake` and the C/C++ compiler toolchain were missing.
6. `numpy==1.26.4` then failed to build from source because Python 3.13 should use a wheel-backed NumPy 2.x release instead.

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
7. If the failure mentions `llama-cpp-python` and `nmake`, either install the Microsoft C++ build tools or skip that dependency on Windows with a platform marker.
8. If the failure mentions `numpy==1.26.4` on Python 3.13, widen the NumPy pin to a wheel-compatible 2.x release.

### Solutions applied in this project

**Issue: `llama-cpp-python` build failure due to missing C++ compiler**

- Problem: CMake failed to find `nmake` because Visual C++ build tools are not installed.
- Fix: Added a platform marker to gate the dependency off Windows.
- Change in `pyproject.toml`: `"llama_cpp_python>=0.2.33; sys_platform != \"win32\""`.
- Result: Package won't install on Windows but code using it can still reference it.

**Issue: `numpy==1.24.1` builds from source on Python 3.13**

- Problem: NumPy 1.24.x has no prebuilt wheels for Python 3.13, so compilation was triggered.
- Fix: Loosened the upper bound to allow NumPy 2.x, which has prebuilt wheels.
- Change in `pyproject.toml`: `"numpy>=1.21,<3.0"` (was `"numpy>=1.21,<1.28"`).
- Result: `uv` now picks numpy 2.x, which installs as a prebuilt wheel.

### Status

✅ **Environment ready for use.**

- Python version: 3.13.10
- Total packages installed: 180
- Virtual environment location: `.venv`
- Installation time: ~4m 30s (varies based on filesystem speed)

### Quick start

1. Activate the virtual environment:
   ```powershell
   Set-Location 'd:\2026\Coursera\4_Generative-AI-with-Python'
   .\.venv\Scripts\Activate.ps1
   ```

2. Verify the environment:
   ```powershell
   python --version
   pip list | head
   ```

3. Run your code or notebooks.

### Maintenance rule

Any future change in this folder should update this changelog with:

- what changed,
- why it changed,
- the exact command used,
- and any new failure or recovery step discovered.
