# FastAPI Dev Setup

This project runs on port `8520` by default.

## 1) Open Terminal In Project Folder

```powershell
cd "D:\2026\Coursera\3_Ultimate Guide to FastAPI and Backend Development Specialization\1_Introduction to FastAPI and Backend Development Fundamentals\02-Getting Started"
```

## 2) Activate Virtual Environment

### PowerShell

```powershell
& "D:\2026\Coursera\3_Ultimate Guide to FastAPI and Backend Development Specialization\0000__venv\fastapi_venv\Scripts\Activate.ps1"
```

### Command Prompt (cmd)

```bat
"D:\2026\Coursera\3_Ultimate Guide to FastAPI and Backend Development Specialization\0000__venv\fastapi_venv\Scripts\activate.bat"
```

## 3) Install Dependencies (first time only)

```powershell
pip install fastapi uvicorn scalar-fastapi
```

## 4) Run The App

### Option A: FastAPI CLI with auto-reload (recommended)

```powershell
python -m fastapi dev .\api-docs.py --port 8520
```

### Option B: Run file directly (uses default port 8520 from code)

```powershell
python .\api-docs.py
```

## 5) Open URLs

- App endpoint: http://127.0.0.1:8520/shipment
	Use this to test the actual API response from your route and confirm business output.
- Swagger UI: http://127.0.0.1:8520/docs
	Use this for interactive testing (Try it out), request/response examples, and quick debugging while building.
- ReDoc: http://127.0.0.1:8520/redoc
	Use this for clean, readable API documentation and sharing endpoint details with teammates.
- Scalar docs: http://127.0.0.1:8520/scalar
	Use this as an alternative API docs UI with a modern layout for exploring endpoints and schemas.

## 6) Stop Server

Press `Ctrl + C` in the terminal.
