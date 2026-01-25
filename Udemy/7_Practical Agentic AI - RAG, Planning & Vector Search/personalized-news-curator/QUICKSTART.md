# Personalized News Curator - Quick Start Guide

## ✅ Project Setup Complete!

Your Personalized News Curator project has been successfully created with all best practices in place.

## 📁 Project Structure

```
personalized-news-curator/
├── venv/                          # Python virtual environment
├── src/
│   ├── __init__.py
│   ├── config.py                  # Configuration management
│   ├── datastore.py               # Article storage & preferences
│   ├── agents/
│   │   ├── __init__.py            # Agent tools (search, rerank)
│   │   └── curator_agent.py       # Main LangChain agent
│   └── api_clients/
│       ├── __init__.py
│       ├── tavily_client.py       # Tavily Search (with mocks)
│       └── openai_client.py       # Groq/OpenAI reranking (with mocks)
├── tests/                         # Test directory (ready for tests)
├── main.py                        # CLI entry point
├── demo.py                        # Demo script (no interaction)
├── test_setup.py                  # Verification test
├── requirements.txt               # Dependencies
├── .env                           # Environment variables (created)
├── .env.example                   # Template
├── .gitignore
└── README.md                      # Full documentation
```

## 🚀 Quick Start

### 1. Activate Virtual Environment (Windows)

```bash
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 2. Run the Demo (No User Input Required)

See the system in action with mock data:

```bash
python demo.py
```

This demonstrates:
- Article search and storage
- User preference tracking
- Article reranking
- System statistics

### 3. Run the Interactive Curator

Start the full interactive experience:

```bash
python main.py
```

Follow the prompts:
1. Enter 3 topics you're interested in
2. View recommended articles
3. Rate each article (1=Like, 0=Neutral, -1=Dislike)
4. Get personalized recommendations based on feedback
5. Optionally add new topics to explore

## ⚙️ Configuration

### Environment Variables (`.env`)

```
OPENAI_API_KEY=sk-your-key-here          # OpenAI API key (only if USE_LLM_RERANK=True)
GROQ_API_KEY=gsk-your-key-here           # Groq API key (only if USE_GROQ_RERANK=True)
TAVILY_API_KEY=tvly-your-key-here        # Tavily Search API key
USE_MOCKS=True                           # Use mock data (True) or real APIs (False)
USE_GROQ_RERANK=True                     # Use Groq LLM rerank
USE_LLM_RERANK=False                     # Use OpenAI LLM rerank
LOG_LEVEL=INFO                           # Logging level
MAX_ARTICLES_PER_TOPIC=5                 # Articles to fetch per search
PREFERENCE_UPDATE_FACTOR=0.1             # How much each rating affects preferences
```

### Using Real APIs

To use real APIs instead of mocks (pick Groq or OpenAI for rerank):

1. Get API keys:
   - [OpenAI API](https://platform.openai.com/api-keys)
   - [Tavily Search API](https://tavily.com/)

2. Update `.env`:
   ```
    TAVILY_API_KEY=tvly-xxxxx
    GROQ_API_KEY=gsk-xxxxx      # or set OPENAI_API_KEY and USE_LLM_RERANK=True
    OPENAI_API_KEY=sk-xxxxx
    USE_MOCKS=False
    USE_GROQ_RERANK=True        # default LLM rerank path
    USE_LLM_RERANK=False        # set True to use OpenAI instead
   ```

3. Run: `python main.py`

## 🎯 Architecture Overview

### Data Flow

```
User Input (Topics)
    ↓
TavilySearchClient.search()  ← Searches for articles
    ↓
ArticleReranker.rerank()     ← Ranks by user preferences
    ↓
ArticleDatastore.add_article() ← Stores with metadata
    ↓
Display Article
    ↓
User Rating (1/-1/0)
    ↓
ArticleDatastore.update_rating() ← Updates preferences
    ↓
Fetch Next Article ← Loop repeats
```

### Key Components

| Component | Purpose | File |
|-----------|---------|------|
| **Article** | Data class for news articles | datastore.py |
| **ArticleDatastore** | In-memory storage with preference tracking | datastore.py |
| **TavilySearchClient** | Search API wrapper (with mocks) | api_clients/tavily_client.py |
| **ArticleReranker** | Rank articles by preferences | api_clients/openai_client.py |
| **NewsCuratorAgent** | Orchestrates user interaction | agents/curator_agent.py |

## 📊 Preference Learning Model

The app uses **linear preference updates**:

```python
preference_score += rating * 0.1
```

**Example:**
- User likes an article about AI → `ai_score += 0.1`
- User dislikes climate article → `climate_score -= 0.1`
- Over 10 likes: score reaches 1.0 (maximum preference)
- Over 10 dislikes: score reaches -1.0 (minimum preference)

This simple model improves recommendations as users provide feedback.

## 🧪 Testing

### Run Verification Test

```bash
python test_setup.py
```

Verifies all imports and basic functionality work.

### Run Demo

```bash
python demo.py
```

Non-interactive demonstration of all features.

## 📚 Learning Outcomes

This project demonstrates:

✅ **LangChain Patterns**
- Agent creation and tool definition
- Agent orchestration for multi-step workflows
- Streaming and response handling

✅ **Agentic AI**
- Autonomous decision-making
- Tool integration
- Context management

✅ **Python Best Practices**
- Virtual environments for isolation
- Modular code organization
- Configuration management with environment variables
- Type hints and documentation

✅ **API Integration**
- Tavily Search API (with mock fallback)
- OpenAI API (with mock fallback)
- Error handling and graceful degradation

✅ **Preference Learning**
- Simple machine learning for personalization
- Linear update models
- Preference aggregation

✅ **CLI Development**
- Interactive command-line interfaces
- User input handling
- Progress indication and feedback

## 🔄 Interaction Flow

### Initial Session

```
1. User enters 3 topics
2. System fetches 1 article per topic (3 total)
3. Articles displayed one-by-one
4. User rates each (Like/Neutral/Dislike)
5. After each rating, 1 new article is fetched
6. User can add new topics or exit
```

### Preference Updates

As users rate articles, the system learns:
- Which topics they prefer
- How much they like/dislike each topic
- What content resonates with them

New articles are reranked based on this growing preference model.

## 🚨 Troubleshooting

### `ModuleNotFoundError: No module named 'src'`

**Solution:** Make sure you're running from the project root directory:
```bash
cd personalized-news-curator
python main.py
```

### `KeyError: 'OPENAI_API_KEY'`

**Solution:** Create `.env` file (copy from `.env.example`):
```bash
copy .env.example .env
```

Or set `USE_MOCKS=True` to use test data.

### Articles not showing up

Check the datastore summary:
```python
from datastore import ArticleDatastore
store = ArticleDatastore()
print(store.summary())
```

## 📝 Next Steps (Future Enhancements)

- [ ] Persistent storage (SQLite/JSON)
- [ ] Vector embeddings for article similarity
- [ ] Exponential smoothing for preferences
- [ ] Email digest generation
- [ ] Web UI (Flask/FastAPI)
- [ ] Multi-user support
- [ ] Article caching
- [ ] Performance monitoring
- [ ] A/B testing different ranking algorithms

## 🔗 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Tavily Search API](https://tavily.com/)
- [OpenAI API](https://platform.openai.com/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## ✨ Key Features

✅ **Mock Data** - Test without API keys  
✅ **Linear Learning** - Simple but effective preference model  
✅ **Article Queue** - Continuous feed with backlog  
✅ **Modular Design** - Easy to extend and modify  
✅ **Error Handling** - Graceful fallbacks for API failures  
✅ **Type Hints** - Clear, maintainable code  
✅ **Well Documented** - Extensive docstrings  

---

**Ready to explore personalized news!** 🗞️
