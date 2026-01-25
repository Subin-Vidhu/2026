# Personalized News Curator with LangChain

A command-line news curation tool that uses LangChain, Tavily Search, and optional Groq/OpenAI reranking to personalize news recommendations based on user preferences.

## Features

- **Interactive CLI**: Easy-to-use command-line interface for discovering news
- **Tavily Search Integration**: Fetch articles from multiple sources
- **LangChain Agent**: Agentic AI for coordinating search and ranking
- **Groq/OpenAI Reranking**: LLM-based ranking (toggleable via .env)
- **Preference Learning**: Linear preference model that improves with feedback
- **Article Queue**: Continuous feed with backlog management

## Project Structure

```
personalized-news-curator/
├── src/
│   ├── config.py              # Configuration and environment management
│   ├── datastore.py           # In-memory article storage
│   ├── agents/
│   │   ├── curator_agent.py   # Main LangChain agent
│   │   └── __init__.py        # Agent tools
│   └── api_clients/
│       ├── tavily_client.py   # Tavily Search API wrapper (with mocks)
│       └── openai_client.py   # Groq/OpenAI reranking (with mocks)
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
└── .gitignore
```

## Installation

### 1. Clone/Download Project

```bash
cd personalized-news-curator
```

### 2. Create Virtual Environment (Windows)

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment

Copy `.env.example` to `.env` and configure:

```bash
copy .env.example .env
```

Edit `.env` with your API keys:

```
OPENAI_API_KEY=sk-your-key-here
GROQ_API_KEY=gsk-your-key-here
TAVILY_API_KEY=tvly-your-key-here
USE_MOCKS=False
USE_GROQ_RERANK=True   # Groq rerank on/off
USE_LLM_RERANK=False   # OpenAI rerank on/off
```

**Note:** The app includes built-in mock data, so you can test without API keys by keeping `USE_MOCKS=True`

## Usage

### Run with Mock Data (No API Keys Required)

```bash
python main.py
```

Follow the prompts:
1. Enter 3 topics of interest
2. View suggested articles
3. Rate each article (Like/Neutral/Dislike)
4. Receive new personalized suggestions
5. Optionally add new topics to explore

### Run with Real APIs

Set `USE_MOCKS=False` in `.env` and provide API keys (choose Groq or OpenAI):

```bash
TAVILY_API_KEY=tvly-xxxxx
GROQ_API_KEY=gsk-xxxxx      # or use OPENAI_API_KEY with USE_LLM_RERANK=True
OPENAI_API_KEY=sk-xxxxx
USE_MOCKS=False
USE_GROQ_RERANK=True        # default LLM rerank path
USE_LLM_RERANK=False        # set True if you want OpenAI instead
```

## Architecture

### Data Flow

```
User Input (Topics)
    ↓
Search Tool (Tavily)
    ↓
Rerank Tool (Groq/OpenAI)
    ↓
Article Datastore
    ↓
Display & Collect Feedback
    ↓
Update Preferences (Linear)
    ↓
Fetch Next Article
    ↓
[Loop]
```

### Key Components

- **Article**: Data class representing a news article with metadata
- **ArticleDatastore**: In-memory storage with preference tracking
- **TavilySearchClient**: Search API wrapper with mock fallback
- **ArticleReranker**: Groq/OpenAI-based ranking with mock fallback
- **NewsCuratorAgent**: Orchestrates the user interaction flow

## Preference Learning

The app uses a **linear preference model**:

```python
preference_score += rating * 0.1
```

Where:
- `rating = 1`: Like (increases preference)
- `rating = 0`: Neutral (no change)
- `rating = -1`: Dislike (decreases preference)

Preferences adjust over time as users provide feedback, improving recommendations.

## Configuration Options

In `.env`:

```
LOG_LEVEL=INFO                    # Logging level
MAX_ARTICLES_PER_TOPIC=5          # Articles to fetch per search
RERANK_THRESHOLD=0.6              # Relevance threshold
USE_MOCKS=True                    # Use mock data (no API calls)
PREFERENCE_UPDATE_FACTOR=0.1      # Linear update factor
```

## Dependencies

- **langchain** - Agent orchestration framework
- **langchain-openai** - OpenAI integration
- **langchain-groq** - Groq integration
- **tavily-python** - Tavily Search API client
- **openai** / **groq** - API SDKs
- **python-dotenv** - Environment variable management
- **pydantic** - Data validation

## Learning Objectives

This project demonstrates:

✅ **LangChain Agent Patterns**: Agent creation, tool definition, agent streaming
✅ **Agentic AI**: Orchestrating multiple tools to solve problems
✅ **API Integration**: Integrating Tavily and OpenAI APIs
✅ **Python Best Practices**: Virtual environments, modular code, configuration management
✅ **Preference Learning**: Simple machine learning for personalization
✅ **CLI Development**: Interactive command-line applications

## Next Steps (Future Enhancements)

- [ ] Persistent storage (JSON/SQLite)
- [ ] Vector embeddings for article similarity
- [ ] More sophisticated preference models (exponential smoothing, clustering)
- [ ] Email digest generation
- [ ] Web interface
- [ ] Multi-user support
- [ ] Article caching
- [ ] Performance monitoring

## License

MIT

## Support

For issues or questions, refer to the LangChain documentation:
- [LangChain Docs](https://python.langchain.com/)
- [Tavily Search API](https://tavily.com/)
- [OpenAI API](https://platform.openai.com/)
