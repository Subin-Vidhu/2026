# ⚡ Quick Start Guide

Get up and running with Personal Health Agent in 5 minutes!

## Prerequisites

- Python 3.10+ installed
- Ollama installed ([ollama.com](https://ollama.com))
- Telegram account (optional, for bot)

## Step 1: Install Ollama & Pull Model

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.com/install.sh | sh

# Pull recommended model
ollama pull qwen2.5:7b

# Start Ollama server
ollama serve
```

Keep this terminal running!

## Step 2: Setup Project

Open a NEW terminal:

```bash
# Clone or extract the project
cd health-agent-mcp

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
nano .env
```

**Minimum required:**
```env
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b
```

### Getting Telegram Bot Token (Optional but Recommended)

1. Open Telegram, search for `@BotFather`
2. Send `/newbot`
3. Follow instructions
4. Copy the token to `.env`

## Step 4: Generate Demo Data

```bash
python scripts/generate_demo_data.py
```

This creates:
- ✅ 3 demo users
- ✅ 90 days of health data per user
- ✅ Medical records
- ✅ Health goals

## Step 5: Run the Application

```bash
python run.py
```

You should see:
```
🏥 Personal Health Agent
============================================================
Starting application on 0.0.0.0:8000

Services:
  • FastAPI Backend
  • MCP Servers (Data Science, Domain Expert, Health Coach)
  • Telegram Bot

API Documentation: http://localhost:8000/docs
============================================================
```

## Step 6: Test It!

### Option A: Via Telegram (Recommended)

1. Open Telegram
2. Search for your bot: `@YourBotName`
3. Send `/start`
4. Try: "Has my sleep improved this month?"

### Option B: Via API

```bash
# Test health check
curl http://localhost:8000/health

# Send a query
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "message": "How is my sleep quality this week?"
  }'

# Get user stats
curl http://localhost:8000/api/users/1/stats
```

### Option C: Via Swagger UI

Open browser: http://localhost:8000/docs

## Example Queries to Try

### 📊 Data Science
- "Has my sleep improved this month?"
- "Show me my heart rate trends"
- "What's my average step count?"

### 🩺 Medical Questions
- "What does my resting heart rate mean?"
- "Is my cholesterol level normal?"
- "Are there any health concerns I should know about?"

### 💪 Health Coaching
- "Help me improve my sleep quality"
- "I want to be more active"
- "How can I stay motivated?"

## Troubleshooting

### "Connection refused to Ollama"

Make sure Ollama is running:
```bash
ollama serve
```

### "Model not found"

Pull the model:
```bash
ollama pull qwen2.5:7b
```

### Telegram bot not responding

1. Check token in `.env` is correct
2. Restart the application
3. Send `/start` to the bot

### Slow responses

- Use a smaller model: `ollama pull llama3.1:8b`
- Update `.env`: `OLLAMA_MODEL=llama3.1:8b`

## What's Next?

✅ Explore the demo data with different queries
✅ Check out the API documentation at `/docs`
✅ Upload your own health data (CSV format)
✅ Customize agent prompts in `app/mcp_client/orchestrator.py`

## Need Help?

- 📖 Read the full README.md
- 🐛 Check logs in terminal output
- 💬 Review example queries above

---

**Ready to explore? Start chatting with your health agent!** 🚀
