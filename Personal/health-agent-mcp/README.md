# 🏥 Personal Health Agent with MCP + Ollama + Telegram

A multi-agent health assistant system built with Model Context Protocol (MCP), FastAPI, and Telegram Bot. Features three specialized AI agents (Data Science, Domain Expert, Health Coach) powered by local LLMs via Ollama.

## 🎯 Features

- **📊 Data Science Agent**: Analyze health trends, generate insights, create visualizations
- **🩺 Domain Expert Agent**: Medical knowledge, interpret metrics, safety checks
- **💪 Health Coach Agent**: Motivational interviewing, goal setting, behavior tracking
- **🔒 100% Local & Private**: All data and LLM processing stays on your machine
- **📱 Telegram Interface**: Easy-to-use chat interface
- **🎨 Demo Data Included**: Pre-populated health data for testing

## 🏗️ Architecture

```
Telegram Bot → FastAPI Backend → MCP Client → [DS, DE, HC Agents] → Ollama LLM
                                              → Shared Data Server
```

## 📋 Prerequisites

- Python 3.10+
- Ollama installed and running
- Telegram Bot Token
- 8GB+ RAM (for running LLM models)

## 🚀 Quick Start

### 1. Install Ollama

```bash
# Linux/Mac
curl -fsSL https://ollama.com/install.sh | sh

# Windows: Download from https://ollama.com/download
```

### 2. Pull Required Models

```bash
ollama pull qwen2.5:7b
# Alternative models you can try:
# ollama pull llama3.1:8b
# ollama pull mistral:7b
```

### 3. Install Python Dependencies

```bash
cd health-agent-mcp
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
nano .env  # Edit with your credentials
```

**Required Environment Variables:**

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b

# Database
DATABASE_URL=sqlite:///./data/health_agent.db

# Optional: For production
# DATABASE_URL=postgresql://user:password@localhost/health_db
```

### 5. Generate Demo Data

```bash
python scripts/generate_demo_data.py
```

This creates:
- 3 demo users with different health profiles
- 90 days of wearable data per user
- Medical records and health goals

### 6. Start Ollama Server

```bash
ollama serve
```

Keep this terminal running.

### 7. Run the Application

Open a new terminal:

```bash
# Start all MCP servers and FastAPI backend
python run.py
```

The application will:
- ✅ Initialize SQLite database
- ✅ Start 4 MCP servers (DS, DE, HC, Data)
- ✅ Launch FastAPI on http://localhost:8000
- ✅ Start Telegram bot
- ✅ API docs available at http://localhost:8000/docs

### 8. Test via Telegram

1. Open Telegram and search for your bot: `@YourBotUsername`
2. Send `/start` to begin
3. Try these example queries:

```
📊 Data Analysis:
- Has my sleep improved this month?
- Show my heart rate trends
- Analyze my weekly activity levels

🩺 Medical Questions:
- What does my resting heart rate of 65 mean?
- Is my cholesterol level normal?
- Should I be concerned about my HRV?

💪 Health Coaching:
- Help me improve my sleep quality
- I want to increase my daily steps
- How can I be more consistent with exercise?
```

## 🎮 Testing Without Telegram

Use the FastAPI endpoints directly:

```bash
# Query the health agent
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "message": "Has my sleep improved this month?"
  }'

# Upload health data
curl -X POST http://localhost:8000/api/upload_data \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "data_type": "wearable",
    "data": {
      "date": "2026-02-04",
      "heart_rate": 68,
      "steps": 9500,
      "sleep_hours": 7.5
    }
  }'

# Get user health stats
curl http://localhost:8000/api/users/1/stats
```

## 📁 Project Structure

```
health-agent-mcp/
├── mcp_servers/                    # MCP Server implementations
│   ├── data_science_agent/
│   │   ├── server.py              # DS agent MCP server
│   │   ├── tools.py               # Analysis tools
│   │   └── __init__.py
│   ├── domain_expert_agent/
│   │   ├── server.py              # Medical expert MCP server
│   │   ├── medical_kb.py          # Knowledge base
│   │   └── __init__.py
│   ├── health_coach_agent/
│   │   ├── server.py              # Coaching MCP server
│   │   ├── coaching_strategies.py
│   │   └── __init__.py
│   └── shared_data_server/
│       ├── server.py              # Data access MCP server
│       └── __init__.py
│
├── app/                           # FastAPI Backend
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration
│   ├── mcp_client/
│   │   ├── client.py              # MCP client wrapper
│   │   ├── orchestrator.py       # Query routing
│   │   └── __init__.py
│   ├── telegram/
│   │   ├── bot.py                 # Telegram bot
│   │   ├── handlers.py            # Message handlers
│   │   └── __init__.py
│   ├── models/
│   │   ├── user.py                # User models
│   │   ├── health_data.py         # Health data schemas
│   │   └── __init__.py
│   ├── database/
│   │   ├── db.py                  # Database connection
│   │   ├── models.py              # SQLAlchemy models
│   │   └── __init__.py
│   └── utils/
│       ├── llm_utils.py           # Ollama helpers
│       └── __init__.py
│
├── data/                          # Demo data storage
│   ├── health_agent.db           # SQLite database
│   ├── wearable_data/            # Generated wearable data
│   ├── medical_records/          # Demo medical records
│   └── user_profiles/            # User profiles
│
├── scripts/
│   └── generate_demo_data.py     # Demo data generator
│
├── tests/
│   ├── test_agents.py
│   └── test_api.py
│
├── run.py                         # Main entry point
├── requirements.txt
├── .env.example
├── docker-compose.yml            # Docker deployment (optional)
└── README.md
```

## 🔧 Configuration Details

### Getting Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Follow instructions to create your bot
4. Copy the token provided
5. Add to `.env` file

### Switching LLM Models

Edit `.env`:

```env
# Faster, less accurate
OLLAMA_MODEL=llama3.1:8b

# Balanced (recommended)
OLLAMA_MODEL=qwen2.5:7b

# More accurate, slower
OLLAMA_MODEL=mixtral:8x7b
```

### Database Options

**SQLite (Default - for demo/testing):**
```env
DATABASE_URL=sqlite:///./data/health_agent.db
```

**PostgreSQL (for production):**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/health_db
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agents.py

# Run with coverage
pytest --cov=app tests/
```

## 🐳 Docker Deployment (Optional)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

## 📊 Demo User Profiles

The system comes with 3 pre-configured demo users:

### User 1: "Active Alice" (ID: 1)
- Age: 32, Female
- Goals: Improve cardio fitness
- Activity: 9000+ steps/day
- Recent trend: Improving heart rate variability

### User 2: "Busy Bob" (ID: 2)
- Age: 45, Male
- Goals: Better sleep quality
- Challenge: Irregular sleep schedule
- Recent trend: Elevated resting heart rate

### User 3: "Senior Sarah" (ID: 3)
- Age: 68, Female
- Goals: Maintain mobility
- Medical: Pre-diabetes, hypertension
- Recent trend: Stable metrics with medication

## 🎯 Example Conversations

### Data Science Query

```
User: Has my resting heart rate improved over the last month?

Agent: 📊 Data Science Agent analyzing...

Based on your wearable data from Jan 5 - Feb 4, 2026:

• Early period (Jan 5-20): Average RHR 72 bpm
• Recent period (Jan 21-Feb 4): Average RHR 68 bpm
• Change: -4 bpm (5.6% improvement) ✅
• Trend: Consistently decreasing
• HRV correlation: +8ms increase (positive sign)

Your cardiovascular fitness is improving! This aligns with 
your increased activity levels (avg 9,200 steps/day vs 
7,800 previously).
```

### Medical Expert Query

```
User: My latest blood work shows cholesterol at 210 mg/dL. 
Should I be worried?

Agent: 🩺 Domain Expert reviewing your results...

Total Cholesterol: 210 mg/dL
• Classification: Borderline High (200-239 range)
• Risk Level: Moderate attention needed

Context from your profile:
✓ Age: 32 (lower risk)
✓ Active lifestyle (9K+ steps/day)
✓ No cardiovascular history
✓ Recent weight: stable

Recommendations:
1. Request full lipid panel (HDL, LDL, triglycerides)
2. HDL >60 mg/dL would offset concern
3. Continue current exercise routine
4. Dietary review: limit saturated fats
5. Retest in 3 months

⚠️ This is educational information, not medical advice. 
Please consult your healthcare provider for personalized guidance.
```

### Health Coach Conversation

```
User: I want to sleep better but I'm always scrolling my 
phone before bed

Agent: 💪 Health Coach here to support you!

I hear you - falling into the phone scroll before bed is 
something many people struggle with. It sounds like you're 
aware this might be affecting your sleep quality.

On a scale of 1-10, how ready do you feel to make a change 
around this?

User: Maybe a 7? I know it's bad but it's hard

Agent: A 7 is actually really good! You're past the halfway 
mark. Let me ask - what makes it a 7 and not, say, a 3?

User: I really notice I sleep worse when I'm on my phone late

Agent: That's powerful self-awareness. You've connected the 
behavior to how you feel. 

What would be one small, doable step you could take tonight? 
Not perfection, just something realistic.

[Continues with motivational interviewing approach...]
```

## 🛠️ Troubleshooting

### Issue: "Ollama connection refused"

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start Ollama
ollama serve
```

### Issue: "Model not found"

**Solution:**
```bash
# Pull the required model
ollama pull qwen2.5:7b

# Verify it's available
ollama list
```

### Issue: "Telegram webhook error"

**Solution:**
```bash
# The bot uses polling, not webhooks
# Ensure TELEGRAM_BOT_TOKEN is correct
# Check bot token with @BotFather
```

### Issue: "MCP server startup failed"

**Solution:**
```bash
# Check Python path in mcp_servers/*/server.py
# Ensure fastmcp is installed
pip install fastmcp

# Test individual server
cd mcp_servers/data_science_agent
python server.py
```

### Issue: "Database locked"

**Solution:**
```bash
# Stop all running instances
pkill -f "python run.py"

# Delete database and regenerate
rm data/health_agent.db
python scripts/generate_demo_data.py
```

## 📈 Performance Optimization

### Speed up responses

1. **Use smaller models:**
   ```env
   OLLAMA_MODEL=llama3.1:8b  # Faster than qwen2.5:7b
   ```

2. **Enable GPU acceleration** (if available):
   ```bash
   # Ollama automatically uses GPU if available
   # Verify with:
   ollama run qwen2.5:7b "test"
   ```

3. **Increase Ollama concurrency:**
   ```bash
   # Set environment variable
   export OLLAMA_NUM_PARALLEL=4
   ollama serve
   ```

## 🔐 Security Considerations

⚠️ **For Demo/Development Only**

This project is for **demonstration and learning purposes**. For production use:

1. ✅ Use HTTPS for FastAPI endpoints
2. ✅ Implement user authentication (JWT tokens)
3. ✅ Add rate limiting
4. ✅ Sanitize all user inputs
5. ✅ Use PostgreSQL instead of SQLite
6. ✅ Encrypt sensitive health data at rest
7. ✅ Implement audit logging
8. ✅ Add CORS properly
9. ✅ Never expose real medical data
10. ✅ Comply with HIPAA/GDPR if handling real patient data

## 🤝 Contributing

Contributions welcome! This is a learning project demonstrating MCP architecture.

## 📄 License

MIT License - See LICENSE file

## 🙏 Acknowledgments

- Based on "The Anatomy of a Personal Health Agent" paper (arXiv:2508.20148)
- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Powered by [Ollama](https://ollama.ai/)
- MCP Protocol by [Anthropic](https://modelcontextprotocol.io/)

## 📞 Support

Issues? Questions? 

1. Check the troubleshooting section above
2. Review logs in `logs/` directory
3. Open an issue on GitHub
4. Check Ollama docs: https://ollama.ai/

---

**Built with ❤️ using FastAPI, MCP, and Ollama**

**Note:** This is a demonstration system for educational purposes. Not intended for real medical use. Always consult healthcare professionals for medical advice.
