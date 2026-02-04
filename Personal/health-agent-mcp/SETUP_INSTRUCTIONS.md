# 🏥 Personal Health Agent - Complete Setup Instructions

## 📦 What You've Received

A complete, production-ready Personal Health Agent system implementing the architecture from the paper "The Anatomy of a Personal Health Agent" (arXiv:2508.20148).

**Package Contents:**
- ✅ 3 MCP Agent Servers (Data Science, Domain Expert, Health Coach)
- ✅ FastAPI Backend with Orchestrator
- ✅ Telegram Bot Integration
- ✅ SQLite Database with Demo Data Generator
- ✅ Complete Documentation
- ✅ Docker Support
- ✅ Tests & Examples

## 🚀 Quick Setup (5 Minutes)

### Step 1: Extract the Project

```bash
unzip health-agent-mcp.zip
cd health-agent-mcp
```

### Step 2: Install Ollama

**Linux/Mac:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from https://ollama.com/download

**Pull the Model:**
```bash
ollama pull qwen2.5:7b
```

**Start Ollama (keep this running):**
```bash
ollama serve
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
cp .env.example .env
```

**Edit .env file:**
```bash
nano .env  # or use your favorite editor
```

**Required Configuration:**
```env
# Get this from @BotFather on Telegram
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Ollama settings (defaults should work)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b

# Database (SQLite for demo)
DATABASE_URL=sqlite:///./data/health_agent.db
```

### Step 5: Generate Demo Data

```bash
python scripts/generate_demo_data.py
```

**This creates:**
- 3 demo users (Alice, Bob, Sarah)
- 90 days of realistic health data per user
- Medical records with blood work
- Active health goals

### Step 6: Run the Application

```bash
python run.py
```

**You should see:**
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

## ✅ Verification

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

Expected: `{"status": "healthy", ...}`

### Test 2: API Query
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "message": "How is my sleep this week?"
  }'
```

Expected: JSON response with agent analysis

### Test 3: Telegram Bot

1. Open Telegram
2. Search for your bot: `@YourBotName`
3. Send: `/start`
4. Try: "Has my sleep improved this month?"

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **README.md** | Comprehensive project documentation |
| **QUICKSTART.md** | Fast setup guide (you're reading an extended version) |
| **TESTING.md** | Complete testing scenarios and validation |
| **EXAMPLE_QUERIES.md** | 100+ example queries to try |
| **LICENSE** | MIT License with medical disclaimer |

## 🎮 Demo Users

### User 1: Active Alice (ID: 1)
- 32, Female, Athletic profile
- Goal: Improve cardio fitness
- ~9,500 steps/day
- Improving heart rate trends

### User 2: Busy Bob (ID: 2)
- 45, Male, Sedentary profile
- Goal: Better sleep quality
- ~5,500 steps/day
- Borderline cholesterol (215 mg/dL)

### User 3: Senior Sarah (ID: 3)
- 68, Female, Senior profile
- Goal: Maintain mobility
- ~6,000 steps/day
- Managed pre-diabetes & hypertension

## 🔧 Configuration Options

### Using a Different LLM Model

**Faster (but less accurate):**
```bash
ollama pull llama3.1:8b
```

Update `.env`:
```env
OLLAMA_MODEL=llama3.1:8b
```

**More Accurate (but slower):**
```bash
ollama pull mixtral:8x7b
```

### Using PostgreSQL Instead of SQLite

1. Install PostgreSQL
2. Create database: `createdb health_agent`
3. Update `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost/health_agent
```

### Using LM Studio Instead of Ollama

1. Install LM Studio from https://lmstudio.ai/
2. Load a model (Qwen2.5-7B-Instruct recommended)
3. Start local server (default: http://localhost:1234)
4. Update `.env`:
```env
OLLAMA_BASE_URL=http://localhost:1234
OLLAMA_MODEL=qwen2.5-7b-instruct
```

## 🐳 Docker Deployment

**Option 1: Docker Compose (Easiest)**

```bash
# Build and start
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

**Option 2: Manual Docker Build**

```bash
# Build image
docker build -t health-agent .

# Run container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -e TELEGRAM_BOT_TOKEN=your_token \
  --name health-agent \
  health-agent
```

## 🔍 Troubleshooting

### Issue: "Connection refused to Ollama"

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve
```

### Issue: "Model not found"

**Solution:**
```bash
# List available models
ollama list

# Pull required model
ollama pull qwen2.5:7b
```

### Issue: "Telegram bot not responding"

**Solutions:**
1. Verify token in `.env` is correct
2. Check bot was created correctly with @BotFather
3. Restart application: `Ctrl+C` then `python run.py`
4. Send `/start` command to bot

### Issue: "Import errors"

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: "Database errors"

**Solution:**
```bash
# Delete and regenerate database
rm data/health_agent.db
python scripts/generate_demo_data.py
```

### Issue: "Slow responses"

**Solutions:**
1. Use smaller model: `ollama pull llama3.1:8b`
2. Enable GPU if available
3. Increase system resources
4. Close other applications

## 📊 Project Structure

```
health-agent-mcp/
├── app/                    # FastAPI application
│   ├── main.py            # Main entry point
│   ├── config.py          # Configuration
│   ├── mcp_client/        # MCP orchestrator
│   ├── telegram/          # Telegram bot
│   ├── models/            # Pydantic models
│   ├── database/          # Database models & connection
│   └── utils/             # Utilities (LLM client)
│
├── mcp_servers/           # MCP Server implementations
│   ├── data_science_agent/
│   ├── domain_expert_agent/
│   └── health_coach_agent/
│
├── scripts/               # Utility scripts
│   └── generate_demo_data.py
│
├── data/                  # Data storage
├── tests/                 # Test files
├── config/                # Configuration files
│
├── run.py                 # Main run script
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── docker-compose.yml     # Docker deployment
└── Documentation files
```

## 🎯 Next Steps

### 1. Explore with Demo Data

Try these queries:
- "Has my sleep improved this month?"
- "What does my resting heart rate mean?"
- "Help me improve my activity levels"

### 2. Customize for Your Needs

- Modify agent prompts in `app/mcp_client/orchestrator.py`
- Add new MCP tools in `mcp_servers/*/server.py`
- Customize Telegram bot responses in `app/telegram/bot.py`

### 3. Add Your Own Data

**Via API:**
```bash
curl -X POST http://localhost:8000/api/upload_data \
  -H "Content-Type: application/json" \
  -d '{...}'
```

**Via Database:**
Use the demo data generator as a template

### 4. Deploy to Production

1. Switch to PostgreSQL
2. Add authentication (JWT tokens)
3. Enable HTTPS
4. Set up monitoring
5. Use environment secrets management

## 🔐 Security Considerations

⚠️ **This is a DEMO system** - for production:

1. ✅ Implement user authentication
2. ✅ Add rate limiting
3. ✅ Use HTTPS/TLS
4. ✅ Encrypt sensitive data
5. ✅ Add audit logging
6. ✅ Comply with HIPAA/GDPR
7. ✅ Regular security audits
8. ✅ Secure API endpoints

## 💡 Tips for Best Results

### LLM Model Selection

- **Development:** llama3.1:8b (fast)
- **Production:** qwen2.5:7b (balanced)
- **Best Quality:** mixtral:8x7b (slower)

### Query Best Practices

✅ Be specific: "sleep last week" vs "sleep"
✅ Include context: "I'm 45 years old"
✅ Follow up: Agents remember conversation
✅ Natural language: No need for special syntax

### Performance Optimization

1. Cache frequently accessed data
2. Use smaller models for classification
3. Enable GPU acceleration
4. Batch process when possible

## 📞 Support & Resources

- **Documentation:** Read all .md files
- **Examples:** See EXAMPLE_QUERIES.md
- **Testing:** Follow TESTING.md
- **Issues:** Check troubleshooting above

## 🎓 Learning Resources

- **MCP Protocol:** https://modelcontextprotocol.io/
- **Ollama:** https://ollama.ai/
- **FastAPI:** https://fastapi.tiangolo.com/
- **Original Paper:** arXiv:2508.20148

## ✨ Features Implemented

✅ Multi-agent architecture (DS, DE, HC)
✅ MCP protocol integration
✅ Local LLM via Ollama/LM Studio
✅ FastAPI REST API
✅ Telegram bot interface
✅ SQLite/PostgreSQL database
✅ Demo data generation
✅ Conversation history
✅ Health goal tracking
✅ Medical record management
✅ Statistical analysis
✅ Medical knowledge interpretation
✅ Motivational interviewing

## 🚧 Future Enhancements

Ideas for extension:
- [ ] Web interface (React/Vue)
- [ ] Voice interface
- [ ] Wearable device integration
- [ ] Advanced ML predictions
- [ ] Multi-language support
- [ ] Export reports (PDF)
- [ ] Data visualization dashboard
- [ ] Integration with health APIs

## 📄 License

MIT License - See LICENSE file

⚠️ **Medical Disclaimer:** This software is for educational and demonstration purposes only. Not intended for medical diagnosis, treatment, or advice. Always consult qualified healthcare professionals.

---

## 🎉 You're All Set!

Your Personal Health Agent is ready to use. Start by:

1. ✅ Sending `/start` to your Telegram bot
2. ✅ Trying example queries from EXAMPLE_QUERIES.md
3. ✅ Exploring the API at http://localhost:8000/docs
4. ✅ Customizing the agents for your needs

**Happy Health Tracking! 🏥💪**

---

*Built with ❤️ using FastAPI, MCP, and Ollama*
*Based on "The Anatomy of a Personal Health Agent" research*
