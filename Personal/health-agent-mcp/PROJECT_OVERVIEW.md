# Personal Health Agent — Beginner Overview

## What this project is
A local-first health assistant that:
- Collects and stores health data (wearables + medical records).
- Routes questions to specialized agents (Data Science, Domain Expert, Health Coach).
- Uses an LLM (Ollama) to explain results in plain language.
- Exposes a FastAPI backend and a Telegram bot interface.

It’s designed for learning and prototyping a multi-agent system with a real backend, storage, and chat interface.

---

## How we set it up (high level)
1) **Python environment + dependencies**
   - `pip install -r requirements.txt`
2) **Ollama + models**
   - Ollama runs on your LAN at `http://192.168.0.18:11444`.
   - Default model: `kimi-k2.5:cloud`
   - Fallback model: `glm-4.7-flash:latest`
3) **App config** (`.env`)
   - `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, `OLLAMA_FALLBACK_MODEL`
   - `TELEGRAM_BOT_TOKEN`
4) **Run**
   - `python run.py`

Logging is automatically saved to `logs/app_DDMMYYYY.log`.

---

## MCP agents (what they are and what they do)
This project uses an **agent-oriented** architecture. Each agent has a specific role and exposes “tools” (functions).

### 1) Data Science Agent (ds)
**Purpose:** Analyze trends and statistics in wearable data.
**Main tools:**
- `analyze_health_trend` — trend detection for a metric over time.
- `compare_metrics` — correlation between two metrics.
- `get_weekly_summary` — weekly stats for all metrics.

### 2) Domain Expert Agent (de)
**Purpose:** Provide medical context and interpret metrics.
**Main tools:**
- `interpret_health_metric` — explains a metric based on ranges.
- `check_health_concerns` — flags potential concerns from recent data.
- `get_medical_context` — summarizes user medical records.

### 3) Health Coach Agent (hc)
**Purpose:** Goal creation and progress tracking.
**Main tools:**
- `create_health_goal` — creates a new user goal.
- `get_active_goals` — lists active goals.
- `track_progress` — shows progress on a goal.

**How they work together:**
The orchestrator (`app/mcp_client/orchestrator.py`) decides which agent to use based on the user’s message and then calls the right tool.

---

## Real‑world use case
This project mirrors how a real digital health product works:
- **Data ingestion** → wearables & records saved in a database.
- **Analysis** → data science functions compute trends.
- **Interpretation** → expert‑style explanations.
- **Coaching** → actionable guidance and goal tracking.
- **Interfaces** → API + Telegram for easy access.

It’s a realistic blueprint for building:
- Personalized health dashboards
- Telehealth companion apps
- Habit coaching platforms
- Wellness analytics bots

---

## How demo data is used
The project ships with a demo data generator (`scripts/generate_demo_data.py`). It creates 3 sample users with 90 days of data.

### Demo data fallback for Telegram
If a Telegram user has no wearable data:
- The system **falls back to demo users** (Active Alice / Busy Bob / Senior Sarah).
- This ensures beginner testing works without manual data entry.

You can switch this off later if you only want real user data.

---

## What gets sent to the LLM
The LLM is used for **natural language explanations**, not raw data crunching.

### Data Science queries
1) MCP tool returns structured analysis.
2) We generate a prompt:
   - User query
   - JSON analysis summary
3) LLM produces a short, friendly explanation.

### Domain Expert queries
1) MCP tools return:
   - Medical context (records)
   - Concerns from recent data
2) We generate a prompt:
   - User question
   - User context JSON
   - Health concerns JSON
3) LLM responds with educational guidance.

### Health Coach queries
1) MCP tools return:
   - Active goals
2) We generate a prompt:
   - Conversation context
   - Active goals JSON
   - Coaching guidance
3) LLM responds with motivational coaching tone.

The LLM **never writes to the database**. It only summarizes and explains.

---

## End‑to‑end flow (simple)
1) Telegram message → `HealthAgentBot`
2) Bot calls `HealthAgentOrchestrator`
3) Orchestrator classifies intent using Ollama
4) Correct MCP tool runs (data/medical/coach)
5) LLM generates user‑friendly response
6) Reply sent to Telegram

---

## Key folders (beginner map)
- `app/` → FastAPI backend + bot + orchestrator
- `mcp_servers/` → agent tool implementations
- `data/` → SQLite DB storage (created at runtime)
- `scripts/` → demo data generator
- `logs/` → runtime logs by date

---

## Quick tips for beginners
- If you see “No data found”, run demo data or re‑/start to seed data.
- If Telegram fails, confirm `TELEGRAM_BOT_TOKEN` in `.env`.
- If Ollama fails, confirm the base URL and model names.

---

## Summary
You now have:
- A multi‑agent health assistant
- An LLM explanation layer
- A Telegram interface
- Realistic demo health data

This is a practical, real‑world architecture for building AI‑powered health assistants.
