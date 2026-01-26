# 🚀 Real Tavily API Setup

## ✅ Status: ENABLED

Your Personalized News Curator is now configured to use **real Tavily API** for fetching actual news articles, with Groq reranking turned on by default (OpenAI optional).

---

## Current Configuration

**File**: `.env`

```properties
TAVILY_API_KEY=tvly-xxxxx
GROQ_API_KEY=gsk-xxxxx
OPENAI_API_KEY=sk-xxxxx          # optional if using OpenAI rerank instead of Groq
USE_MOCKS=False                  # Real API enabled
USE_GROQ_RERANK=True             # Default LLM rerank path
USE_LLM_RERANK=False             # Switch to True if you prefer OpenAI
```

---

## What This Means

| Feature | Before (Mocks) | Now (Real API) |
|---------|---|---|
| **Article Sources** | Pre-generated test data | Live Tavily Search results |
| **Freshness** | Static, same articles | Current news from the web |
| **Accuracy** | Example titles/content | Real news articles |
| **Reranking** | Heuristic mock | Groq (default) or OpenAI LLM |
| **API Calls** | None (offline) | Tavily + Groq/OpenAI (if enabled) |

---

## How It Works

### 1. **Demo Mode** (Automated)
```bash
python demo.py
```
- Fetches 3 real articles (AI, Climate, Technology)
- Simulates user ratings automatically
- Shows preference updates
- No user interaction needed

### 2. **Interactive Mode** (Full Experience)
```bash
python main.py
```
- Prompts you to enter 3 topics
- Fetches real articles on those topics
- You rate each article (Like/Dislike/Neutral)
- System learns your preferences
- Fetches more articles based on feedback

### 3. **Programmatic Mode** (Code Examples)
```bash
python examples.py
```
- Example 1: Fetches real articles programmatically
- All other examples work with real data

---

## Example Real Article Output

When you run with real API, you'll see actual news like:

```
📰 Title: Anthropic's Claude 3 Opus Sets New AI Benchmark Standards
   URL: https://techcrunch.com/2026/01/...
   Topic: artificial intelligence
   Summary: Anthropic released Claude 3 Opus today, demonstrating 
            significant improvements in reasoning and coding tasks...
   Tags: ['AI', 'Claude', 'LLM']

   Rate: [1] Like [0] Neutral [-1] Dislike [m] Menu
```

Real articles with real URLs and current information!

---

## API Key Details

**Tavily API Key**: `tvly-xxxxx`
- ✅ Required for real search
- ✅ Supports up to 100 API calls/day (free tier)

**Groq API Key**: `gsk-xxxxx`
- ✅ Used when `USE_GROQ_RERANK=True`
- ✅ Default LLM rerank path

**OpenAI API Key**: `sk-xxxxx`
- ✅ Optional; set `USE_LLM_RERANK=True` if you prefer OpenAI rerank
- ✅ Mock rerank is used if LLM rerank fails

---

## Cost Considerations

### Tavily API
- **Free Tier**: 100 searches/day
- **Cost**: $0 (developer testing)
- **Typical Usage**: ~1 search per 3 articles
- **Demo Cost**: ~0.03¢ (3 searches)

### Groq / OpenAI (Reranking)
- **Groq**: Default LLM rerank when `USE_GROQ_RERANK=True`; low cost on free tier
- **OpenAI**: Enable with `USE_LLM_RERANK=True`; costs depend on model pricing
- **Fallback**: If LLM rerank errors, heuristic rerank is used

---

## Testing the Real API

### Quick Test (30 seconds)
```bash
python demo.py
```
See real articles being fetched instantly.

### Full Interactive Test
```bash
python main.py
```
Enter topics like:
- `artificial intelligence`
- `climate change`
- `space exploration`
- `quantum computing`
- `blockchain`

---

## Troubleshooting

### Issue: "API Key Invalid"
**Solution**: Check `.env` file has correct keys

### Issue: "API Rate Limit Exceeded"
**Solution**: You've exceeded 100 calls/day on free tier
- **Wait until tomorrow**, or
- **Upgrade to paid plan**, or
- **Switch back to MOCKS**: `USE_MOCKS=True`

### Issue: "Network Error"
**Solution**: Check internet connection
- Tavily requires working internet
- Fallback to mocks: `USE_MOCKS=True`

---

## Switching Between Real and Mock

### To Use Real API (Current)
```properties
USE_MOCKS=False
```

### To Use Mocks (If API Rate Limited)
```properties
USE_MOCKS=True
```

Just edit `.env` and save!

---

## Next Steps

### 1. **Try it out!**
```bash
python main.py
```

### 2. **Explore real articles**
- See how Tavily searches work
- Notice topic relevance
- Rate articles to learn preferences

### 3. **Understand the flow**
- Real articles are fetched from Tavily
- Stored in in-memory datastore
- Reranked based on preferences
- Continuous feedback loop

### 4. **Optional: Persistent Storage**
Future enhancement: Save articles to SQLite instead of memory

---

## Key Differences from Mocks

| Aspect | Mock | Real |
|--------|------|------|
| **Sources** | Pre-set examples | Web search results |
| **Topics** | Limited set | Any topic Tavily knows |
| **Relevance** | Always matches | Varies by search |
| **URLs** | Fake URLs | Real links |
| **Content** | Generated examples | Real article text |
| **Updates** | Static | Current news |

---

## API Limits & Usage

**Tavily Free Tier**: 100 searches/day
- Each topic = 1 search
- Demo: 3 searches
- Interactive session: 1-10 searches depending on usage

**Track your usage:**
```bash
python examples.py  # Uses 1 search
python demo.py      # Uses 3 searches
python main.py      # Uses 1 search per topic + 1 Groq/OpenAI call per rerank (if enabled)
```

---

## Features Now Available

✅ **Real News Articles** - From Tavily Search  
✅ **Actual Web URLs** - Click-through to read full articles  
✅ **Current Information** - Today's news, not examples  
✅ **Topic Flexibility** - Search any topic imaginable  
✅ **LLM Reranking** - Groq (default) or OpenAI, with heuristic fallback  
✅ **Preference Learning** - Build model from real articles  
✅ **Feedback Loop** - Rate real articles → get relevant results  

---

## Remember

- 🔐 **API keys are in `.env`** - Keep it private!
- 📡 **Requires internet** - Won't work offline
- 📊 **Limited to 100/day** - Plan usage accordingly
- 🎯 **Try different topics** - Explore Tavily's capabilities
- 💾 **Articles stay in memory** - Exit program = lose history

---

## Go Live!

```bash
python main.py
```

Enjoy personalized news with real, current articles! 🗞️

