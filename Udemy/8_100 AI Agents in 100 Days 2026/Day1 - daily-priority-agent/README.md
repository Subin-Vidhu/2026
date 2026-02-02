# Daily Priority Agent (Day 1)

**AI Agent Challenge**: 100 AI Agents in 100 Days - Day 1

## Overview

A smart task prioritization agent that analyzes your tasks and generates an intelligent daily plan. It scores tasks based on urgency, importance, effort, and blockers to help you focus on what matters most.

## Features

- **Smart Scoring Algorithm**: Combines multiple factors (urgency, importance, effort, blockers)
- **Automatic Categorization**: Separates tasks into TOP 3, NEXT 5, UNBLOCK, and DEFER
- **Quick Win Detection**: Prioritizes tasks that take ≤15 minutes
- **Deadline Awareness**: Automatically calculates urgency based on due dates
- **Blocked Task Handling**: Identifies and flags tasks waiting on dependencies
- **Impact Analysis**: Weights tasks by their importance (low, medium, high)
- **Multiple Output Formats**: Generates both JSON (plan.json) and human-readable (plan.txt) outputs

## How It Works

### Scoring Algorithm

Each task receives a score based on:

```
Score = (Urgency × 3.0) + (Importance × 4.0) + Quick Win Bonus - Blocked Penalty
```

- **Urgency** (0-5 scale):
  - 5.0: Overdue or due today
  - 4.0: Due tomorrow
  - 3.0: Due within 3 days
  - 2.0: Due within 7 days
  - 1.0: Due later
  - 0.5: No deadline

- **Importance** (1-3 scale):
  - 3: High impact
  - 2: Medium impact
  - 1: Low impact

- **Quick Win Bonus**: +1.0 for tasks ≤15 minutes
- **Blocked Penalty**: -5.0 for blocked tasks

### Task Categories

1. **TOP 3**: Highest priority unblocked tasks (do these first!)
2. **NEXT 5**: Next set of important tasks
3. **UNBLOCK**: Blocked tasks requiring dependencies to be resolved
4. **DEFER**: Low urgency + low impact tasks for later

## Usage

### 1. Prepare Your Tasks

Edit `tasks.csv` with your tasks:

```csv
title,description,deadline,effort,impact,blocked,tags
Send proposal to client,Finalize and email proposal,2026-02-03,25m,high,no,work
Pay electricity bill,Online payment,2026-02-03,10m,medium,no,personal
Book dentist appointment,Call dentist office,,10m,low,no,personal
```

**Field Specifications:**

- **title**: Task name (required)
- **description**: Brief description
- **deadline**: Due date in YYYY-MM-DD format (optional)
- **effort**: Time estimate
  - `S` = 15 min
  - `M` = 45 min (default)
  - `L` = 90 min
  - Or specify: `25m`, `60min`, `30`
- **impact**: `low`, `medium`, or `high`
- **blocked**: `yes`/`no` - Is this task blocked by dependencies?
- **tags**: Comma-separated tags (e.g., `work,urgent`)

### 2. Run the Agent

```bash
python agent.py
```

### 3. Review Your Plan

The agent generates two files:

- **plan.json**: Structured data with full scoring breakdown
- **plan.txt**: Human-readable daily plan

**Example Output:**

```
Daily Task Prioritization Plan (2026-02-02)
=============================================

TOP 3 (Do these first)
----------------------
1. Send proposal to client  | deadline: 2026-02-03 | effort: 25m | score: 27.0
   Why: Due soon, High impact
2. Pay electricity bill  | deadline: 2026-02-03 | effort: 10m | score: 23.0
   Why: Due soon, Medium impact, Quick win
3. Prepare meeting agenda  | deadline: 2026-02-04 | effort: 30m | score: 21.0
   Why: Due soon, High impact

NEXT 5
------
...

UNBLOCK (Blocked tasks)
-----------------------
1. Wait for design assets  | deadline: 2026-02-03 | effort: 15m | score: 22.0
   Why: Due soon, High impact, Quick win, Blocked (needs unblock step)
```

## Configuration

Adjust weights and defaults in `agent.py`:

```python
EFFORT_DEFAULTS_MIN = {"S": 15, "M": 45, "L": 90}
IMPACT_MAP = {"low": 1, "medium": 2, "high": 3}

WEIGHTS = {
    "urgency": 3.0,        # Weight for deadline urgency
    "importance": 4.0,     # Weight for task impact
    "quickwin_bonus": 1.0, # Bonus for tasks ≤15 min
    "blocked_penalty": 5.0, # Penalty for blocked tasks
}

TOP3_COUNT = 3  # Number of top priority tasks
NEXT5_COUNT = 5 # Number of next tasks
```

## Example Scenarios

### Scenario 1: Urgent with High Impact
- Task: "Send proposal to client"
- Deadline: Tomorrow
- Effort: 25 minutes
- Impact: High
- **Result**: Appears in TOP 3

### Scenario 2: Quick Win
- Task: "Pay electricity bill"
- Deadline: Tomorrow
- Effort: 10 minutes (Quick win!)
- Impact: Medium
- **Result**: Gets bonus points, prioritized higher

### Scenario 3: Blocked Task
- Task: "Wait for design assets"
- Blocked: Yes
- **Result**: Moved to UNBLOCK section despite high score

### Scenario 4: Low Priority
- Task: "Clean downloads folder"
- Deadline: None
- Impact: Low
- **Result**: Moved to DEFER section

## Benefits

- **Save Decision Fatigue**: Let the algorithm decide what's most important
- **Never Miss Deadlines**: Automatic urgency calculation
- **Optimize Your Day**: Focus on high-impact work first
- **Quick Wins First**: Build momentum with fast completions
- **Visualize Dependencies**: See what's blocked and needs unblocking
- **Data-Driven**: Transparent scoring with full breakdown

## Files

- `agent.py`: Main prioritization agent
- `tasks.csv`: Input task list
- `plan.json`: Structured output with scoring details
- `plan.txt`: Human-readable daily plan
- `README.md`: This file

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Tips

1. **Review Daily**: Run the agent each morning to plan your day
2. **Update Status**: Mark completed tasks in tasks.csv
3. **Adjust Weights**: Tune the scoring to match your priorities
4. **Track Progress**: Use tags to categorize and analyze your work patterns
5. **Unblock First**: Focus on resolving blockers to unlock dependent tasks

## Future Enhancements

- [ ] Task completion tracking
- [ ] Historical analytics
- [ ] Calendar integration
- [ ] Recurring task support
- [ ] Multi-day planning
- [ ] Task dependencies visualization
- [ ] Mobile notifications

---

**Day 1 of 100** | Building practical AI agents one day at a time 🚀
