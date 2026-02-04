# 🧪 Testing Guide

Complete testing scenarios for the Personal Health Agent.

## Prerequisites

1. Application is running (`python run.py`)
2. Demo data is generated (`python scripts/generate_demo_data.py`)
3. Ollama is running with qwen2.5:7b

## Test Scenarios

### Scenario 1: Data Science Agent

**User:** Active Alice (ID: 1)

#### Query 1: Sleep Analysis
```
"Has my sleep improved this month?"
```

**Expected Response:**
- Agent: Data Science
- Analysis of sleep trends over 30 days
- Comparison of early vs recent period
- Statistical insights (average, trend direction)

#### Query 2: Activity Trends
```
"What's my average step count over the last week?"
```

**Expected Response:**
- Weekly step analysis
- Daily averages
- Activity patterns

#### Query 3: Heart Rate Analysis
```
"Show me my resting heart rate trends"
```

**Expected Response:**
- Heart rate trend analysis
- Improvement/decline indicators
- Context about cardiovascular fitness

### Scenario 2: Domain Expert Agent

**User:** Busy Bob (ID: 2)

#### Query 1: Medical Interpretation
```
"My latest blood work shows cholesterol at 215 mg/dL. Should I be worried?"
```

**Expected Response:**
- Agent: Domain Expert
- Classification of cholesterol level (borderline high)
- Risk assessment based on user profile
- Recommendations
- Disclaimer about medical advice

#### Query 2: Health Concerns
```
"Are there any health concerns I should know about?"
```

**Expected Response:**
- Recent data analysis
- Identified concerns (if any)
- Specific recommendations
- When to consult healthcare provider

#### Query 3: Metric Interpretation
```
"What does a resting heart rate of 75 mean for someone my age?"
```

**Expected Response:**
- Age-appropriate normal ranges
- Status of current heart rate
- Context and implications

### Scenario 3: Health Coach Agent

**User:** Senior Sarah (ID: 3)

#### Query 1: Goal Setting
```
"I want to maintain my mobility and stay active"
```

**Expected Response:**
- Agent: Health Coach
- Empathetic acknowledgment
- Open-ended questions about motivation
- Goal exploration

#### Query 2: Motivation
```
"I'm having trouble staying consistent with my walking"
```

**Expected Response:**
- Motivational interviewing approach
- Reflective listening
- Support for self-efficacy
- Collaborative problem-solving

#### Query 3: Progress Check
```
"How am I doing with my health goals?"
```

**Expected Response:**
- Current goals review
- Progress assessment
- Celebration of efforts
- Encouragement

### Scenario 4: Multi-Agent Queries

**User:** Any

#### Query 1: Comprehensive Health Overview
```
"Give me a comprehensive overview of my health"
```

**Expected Response:**
- Agent: Multi-Agent
- Data science insights (trends)
- Medical expert insights (concerns)
- Health coach insights (goals)
- Holistic recommendations

#### Query 2: Complex Question
```
"My sleep has been bad and my heart rate seems high. What's going on and what should I do?"
```

**Expected Response:**
- Multi-agent collaboration
- Data analysis of both metrics
- Medical interpretation
- Coaching support
- Actionable recommendations

## API Testing

### Test Health Check

```bash
curl http://localhost:8000/health
```

**Expected:**
```json
{
  "status": "healthy",
  "mcp_servers_running": true,
  "telegram_bot_active": true
}
```

### Test Query Endpoint

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "message": "Has my sleep improved this month?"
  }'
```

**Expected:**
```json
{
  "agent": "Data Science",
  "response": "Based on your sleep data...",
  "data": { ... },
  "timestamp": "2026-02-04T..."
}
```

### Test User Stats

```bash
curl http://localhost:8000/api/users/1/stats
```

**Expected:**
```json
{
  "user_id": 1,
  "total_data_points": 90,
  "latest_heart_rate": 58,
  "avg_steps_30d": 9500.0,
  "avg_sleep_30d": 7.5,
  "active_goals": 1
}
```

### Test Upload Data

```bash
curl -X POST http://localhost:8000/api/upload_data \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "data_type": "wearable",
    "data": {
      "date": "2026-02-04T10:00:00",
      "heart_rate": 65,
      "steps": 10000,
      "sleep_hours": 8.0
    }
  }'
```

**Expected:**
```json
{
  "success": true,
  "message": "Wearable data uploaded successfully"
}
```

### Test Create Goal

```bash
curl -X POST http://localhost:8000/api/users/1/goals \
  -H "Content-Type: application/json" \
  -d '{
    "goal_type": "sleep",
    "description": "Get 8 hours of sleep per night",
    "target_value": 8.0,
    "timeline_days": 30
  }'
```

**Expected:**
```json
{
  "success": true,
  "goal_id": 4,
  "message": "Goal created successfully"
}
```

## Telegram Bot Testing

### Basic Commands

1. `/start` - Should show welcome message with keyboard
2. `/help` - Should show help information
3. `/stats` - Should show weekly summary
4. `/goals` - Should show active goals

### Conversation Flow Test

**Test Scenario: Sleep Improvement Journey**

1. User: "I'm not sleeping well"
   - Expected: Health Coach response with empathy

2. User: "I usually get about 6 hours"
   - Expected: Acknowledgment and exploration

3. User: "I want to sleep better"
   - Expected: Goal-setting conversation

4. User: "Has my sleep gotten any better?"
   - Expected: Data Science analysis

5. User: "What does poor sleep mean for my health?"
   - Expected: Domain Expert medical insights

## Performance Testing

### Response Time Expectations

- Simple queries: < 5 seconds
- Complex multi-agent: < 10 seconds
- Data analysis: < 5 seconds

### Load Testing (Optional)

```bash
# Install apache bench
sudo apt-get install apache2-utils

# Test 100 requests, 10 concurrent
ab -n 100 -c 10 -p query.json -T application/json \
  http://localhost:8000/api/query
```

## Error Scenarios

### Test 1: Invalid User ID

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 9999,
    "message": "Test query"
  }'
```

**Expected:** Should handle gracefully with appropriate error message

### Test 2: Ollama Not Running

1. Stop Ollama: `pkill ollama`
2. Try query
3. **Expected:** Error message about LLM unavailability

### Test 3: Missing Data

**Query:** "Analyze my data from last year"

**Expected:** Appropriate message about data availability

## Validation Checklist

After running all tests, verify:

- [ ] All 3 agents respond correctly
- [ ] Multi-agent collaboration works
- [ ] Telegram bot responds to commands
- [ ] API endpoints return expected data
- [ ] Database operations work
- [ ] Error handling is appropriate
- [ ] Response times are acceptable
- [ ] Medical disclaimers are included
- [ ] Conversation history is maintained

## Debugging Tips

### Check Logs

```bash
# Application logs in terminal output
# Look for errors in red text

# Check database
sqlite3 data/health_agent.db "SELECT COUNT(*) FROM users;"
```

### Verify MCP Servers

```bash
# Test individual MCP server
cd mcp_servers/data_science_agent
python server.py
# Should start without errors
```

### Test LLM Connection

```bash
# Test Ollama directly
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:7b",
  "prompt": "Hello",
  "stream": false
}'
```

## Success Criteria

✅ All test scenarios pass
✅ API returns expected responses
✅ Telegram bot is responsive
✅ MCP servers communicate properly
✅ Database operations succeed
✅ Error handling works
✅ Performance is acceptable

---

**Happy Testing! 🧪**
