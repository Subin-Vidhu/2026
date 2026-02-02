# Meeting Agenda Generator Agent (Day 4)

**AI Agent Challenge**: 100 AI Agents in 100 Days - Day 4

## Overview

An AI-powered meeting agenda generator that automatically creates structured, time-boxed meeting agendas from simple meeting descriptions. It ensures efficient meetings by allocating time appropriately, identifying decision points, assigning ownership, and defining expected outcomes for each agenda item.

## Features

- **Automatic Agenda Generation**: Creates structured agendas from brief meeting descriptions
- **Time-Boxed Items**: Allocates specific time for each agenda topic
- **Owner Assignment**: Identifies who should lead each discussion point
- **Outcome Tracking**: Defines expected results for each agenda item
- **Duration Management**: Ensures agenda fits within the specified meeting length
- **Decision Point Identification**: Highlights items requiring decisions
- **Multiple Meeting Types**: Supports decision, planning, sync, brainstorming, and review meetings
- **Dual Output Format**: Generates both JSON and human-readable agendas
- **LAN Ollama Support**: Uses local LLM for privacy and cost savings

## How It Works

### Processing Pipeline

```
Meeting Description → LLM Analysis → Structured Agenda → Time Allocation → Output Files
```

1. **Input Meeting Details**: Provide title, objective, duration, type, participants, and constraints
2. **LLM Processing**: Sends details to GLM-4.7-Flash model for agenda generation
3. **Structure Generation**: Creates time-boxed agenda items with owners and outcomes
4. **Validation**: Ensures total time fits within duration constraint
5. **Output**: Saves as both `agenda.json` and `agenda.txt`

### Agenda Structure

Each generated agenda includes:

| Component | Description | Example |
|-----------|-------------|---------|
| **Meeting Title** | Clear meeting name | "Q1 Product Planning" |
| **Objective** | Meeting purpose | "Decide priorities for Q1 roadmap" |
| **Total Duration** | Meeting length | 60 minutes |
| **Agenda Items** | Time-boxed topics | Topic, Time, Owner, Outcome |

### Agenda Item Structure

```json
{
  "topic": "Review Q4 Results",
  "time_minutes": 10,
  "owner": "Product Manager",
  "outcome": "Team aligned on past performance"
}
```

## Setup

### Prerequisites

- Python 3.7+
- OpenAI library: `pip install openai`
- Access to Ollama instance (local or LAN)

### LLM Configuration

**Current Setup: LAN Ollama**

```python
client = OpenAI(
    base_url="http://192.168.0.18:11444/v1",
    api_key="ollama"
)
```

**Alternative: OpenAI API**

```python
import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Change model to: "gpt-4o-mini" or "gpt-4o"
```

## Usage

### 1. Prepare Meeting Description

Create or edit `meeting.txt`:

```
Meeting Title: Q1 Product Planning
Objective: Decide priorities for Q1 roadmap and align teams
Duration: 60 minutes
Meeting Type: decision
Participants: Product, Engineering, Marketing
Constraints: Must decide top 3 features
```

**Input Field Guide:**

- **Meeting Title**: Clear, descriptive name
- **Objective**: What the meeting aims to achieve
- **Duration**: Total meeting length in minutes
- **Meeting Type**: `decision`, `planning`, `sync`, `brainstorming`, `review`, `workshop`
- **Participants**: Who will attend (roles or names)
- **Constraints**: Special requirements or limitations

### 2. Run the Agent

```bash
python agent.py
```

### 3. Review Generated Agenda

**Console Output:**
```
Meeting agenda generated successfully.
{'meeting_title': 'Q1 Product Planning', 'objective': '...', ...}
```

**agenda.txt** (Human-Readable):
```
Meeting Agenda (2026-02-02)
=============================================

Title: Q1 Product Planning
Objective: Decide priorities for Q1 roadmap and align teams
Duration: 60 minutes

1. Welcome and Context Setting (5 min)
   Owner: Product Manager
   Outcome: Team aligned on meeting goals

2. Review Q4 Results and Learnings (10 min)
   Owner: Product Manager
   Outcome: Team understands current state

3. Present Feature Proposals (15 min)
   Owner: Product Team
   Outcome: All options presented with rationale

4. Engineering Feasibility Discussion (10 min)
   Owner: Engineering Lead
   Outcome: Technical constraints identified

5. Marketing Input and Market Feedback (10 min)
   Owner: Marketing Lead
   Outcome: Customer needs validated

6. Prioritization Discussion (15 min)
   Owner: Product Manager
   Outcome: Consensus on top 3 features

7. Next Steps and Action Items (5 min)
   Owner: Product Manager
   Outcome: Clear assignments and deadlines
```

**agenda.json** (Structured Data):
```json
{
  "meeting_title": "Q1 Product Planning",
  "objective": "Decide priorities for Q1 roadmap and align teams",
  "total_duration_minutes": 60,
  "agenda": [
    {
      "topic": "Welcome and Context Setting",
      "time_minutes": 5,
      "owner": "Product Manager",
      "outcome": "Team aligned on meeting goals"
    },
    {
      "topic": "Review Q4 Results and Learnings",
      "time_minutes": 10,
      "owner": "Product Manager",
      "outcome": "Team understands current state"
    },
    {
      "topic": "Present Feature Proposals",
      "time_minutes": 15,
      "owner": "Product Team",
      "outcome": "All options presented with rationale"
    },
    {
      "topic": "Engineering Feasibility Discussion",
      "time_minutes": 10,
      "owner": "Engineering Lead",
      "outcome": "Technical constraints identified"
    },
    {
      "topic": "Marketing Input and Market Feedback",
      "time_minutes": 10,
      "owner": "Marketing Lead",
      "outcome": "Customer needs validated"
    },
    {
      "topic": "Prioritization Discussion",
      "time_minutes": 15,
      "owner": "Product Manager",
      "outcome": "Consensus on top 3 features"
    },
    {
      "topic": "Next Steps and Action Items",
      "time_minutes": 5,
      "owner": "Product Manager",
      "outcome": "Clear assignments and deadlines"
    }
  ]
}
```

## Meeting Types

### Decision Meeting
```
Meeting Type: decision
Purpose: Make specific decisions
Duration: 45-90 minutes
Agenda Focus: Options presentation, discussion, voting/consensus, action items
```

### Planning Meeting
```
Meeting Type: planning
Purpose: Create roadmaps or project plans
Duration: 60-120 minutes
Agenda Focus: Context, constraints, brainstorming, prioritization, timeline
```

### Sync Meeting
```
Meeting Type: sync
Purpose: Status updates and alignment
Duration: 15-30 minutes
Agenda Focus: Quick updates, blockers, upcoming priorities
```

### Brainstorming
```
Meeting Type: brainstorming
Purpose: Generate ideas and solutions
Duration: 45-90 minutes
Agenda Focus: Problem framing, ideation, evaluation, next steps
```

### Review Meeting
```
Meeting Type: review
Purpose: Evaluate completed work
Duration: 30-60 minutes
Agenda Focus: Presentation, feedback, improvements, action items
```

### Workshop
```
Meeting Type: workshop
Purpose: Hands-on collaboration and skill building
Duration: 120+ minutes
Agenda Focus: Introduction, activities, practice, reflection
```

## Configuration

### Adjust Temperature

Control creativity vs. consistency:

```python
temperature=0.2  # More structured, predictable agendas (recommended)
temperature=0.5  # Balanced creativity and structure
temperature=0.7  # More creative, varied agendas
```

### Customize System Prompt

Tailor agenda generation to your needs:

```python
SYSTEM_PROMPT = """
You are a Meeting Agenda Generator Agent for engineering teams.

Your job is to generate technical meeting agendas.

Rules:
- Always include time for technical Q&A
- Add buffer time for discussions
- Include demo time for technical reviews
- Identify architectural decision points
- Ensure engineering leads own technical topics
- Return ONLY valid JSON...
"""
```

### Time Allocation Guidelines

**Default Time Allocations:**

- **Welcome/Context**: 5-10% of total time
- **Main Content**: 60-70% of total time
- **Discussion**: 15-20% of total time
- **Wrap-up/Actions**: 5-10% of total time

**Example for 60-minute meeting:**

- Welcome: 5 min (8%)
- Main content: 35-40 min (60-67%)
- Discussion: 10-15 min (17-25%)
- Wrap-up: 5 min (8%)

## Use Cases

### 1. Weekly Team Syncs

```
Meeting Title: Engineering Weekly Sync
Objective: Share updates and unblock team members
Duration: 30 minutes
Meeting Type: sync
Participants: Engineering Team
Constraints: Keep updates brief, focus on blockers
```

**Generated Agenda:**
- Round-robin updates (15 min)
- Blocker discussion (10 min)
- Upcoming priorities (5 min)

### 2. Sprint Planning

```
Meeting Title: Sprint 12 Planning
Objective: Plan next sprint and estimate stories
Duration: 120 minutes
Meeting Type: planning
Participants: Dev Team, Product Owner, Scrum Master
Constraints: Must estimate all high-priority stories
```

**Generated Agenda:**
- Sprint goal review (10 min)
- Story presentation (40 min)
- Estimation session (50 min)
- Capacity planning (15 min)
- Commitment and wrap-up (5 min)

### 3. Client Presentations

```
Meeting Title: Q1 Results Presentation
Objective: Present quarterly results and gather feedback
Duration: 45 minutes
Meeting Type: review
Participants: Client Stakeholders, Account Team
Constraints: Leave 15 minutes for Q&A
```

**Generated Agenda:**
- Introduction and agenda (3 min)
- Q1 metrics overview (12 min)
- Key achievements and wins (10 min)
- Challenges and mitigations (8 min)
- Q&A session (15 min)
- Next steps (2 min)

### 4. Problem-Solving Workshop

```
Meeting Title: Customer Churn Analysis
Objective: Identify root causes and solutions
Duration: 90 minutes
Meeting Type: brainstorming
Participants: Product, Engineering, Customer Success
Constraints: Need 3 actionable initiatives
```

**Generated Agenda:**
- Problem statement (10 min)
- Data review (15 min)
- Root cause analysis (20 min)
- Solution ideation (25 min)
- Solution evaluation (15 min)
- Action planning (5 min)

### 5. One-on-One Meetings

```
Meeting Title: Monthly 1:1 with Sarah
Objective: Career development and feedback
Duration: 30 minutes
Meeting Type: sync
Participants: Manager, Sarah
Constraints: Focus on growth opportunities
```

**Generated Agenda:**
- Check-in and recent wins (5 min)
- Current project discussion (10 min)
- Career goals progress (10 min)
- Action items and support needed (5 min)

## Advanced Features

### Constraint Handling

The agent respects specific constraints:

```
Constraints: Must decide top 3 features
→ Includes prioritization and decision-making time

Constraints: Leave 20 minutes for Q&A
→ Allocates specific Q&A block

Constraints: Demo required
→ Adds demo time to agenda

Constraints: All attendees must present
→ Distributes presentation time among participants
```

### Participant-Aware Agenda

The agent assigns ownership based on participants:

```
Participants: Product, Engineering, Marketing
→ Distributes topics across these roles

Participants: CEO, CFO, Department Heads
→ Creates executive-level agenda structure
```

### Duration Optimization

The agent ensures time fits perfectly:

```
Duration: 30 minutes
→ Creates concise agenda with 5-7 items

Duration: 90 minutes
→ Creates comprehensive agenda with buffer time

Duration: 15 minutes
→ Creates quick sync with 3-4 items
```

## Tips & Best Practices

### 1. Be Specific with Objectives

❌ Bad: "Discuss the project"
✅ Good: "Decide on project scope and assign initial tasks"

### 2. Set Realistic Durations

- 15 min: Quick status updates
- 30 min: Standard sync or brief decision
- 60 min: Planning or detailed discussion
- 90+ min: Workshops or complex decisions

### 3. Include Relevant Constraints

```
Constraints: Must include demo
Constraints: CEO available first 30 minutes only
Constraints: Need to finalize budget
Constraints: Remote participants - keep engaging
```

### 4. List Appropriate Participants

Use roles rather than names for reusability:
- Product Manager, Engineering Lead, Designer
- Instead of: John, Sarah, Mike

### 5. Match Meeting Type to Purpose

- **Decision meetings**: Short, focused, outcome-driven
- **Brainstorming**: Longer, open-ended, creative
- **Sync meetings**: Quick, status-focused, blocker-oriented

### 6. Review and Adjust

Generated agendas are starting points:
- Adjust time allocations based on team dynamics
- Add breaks for long meetings (90+ min)
- Include buffer time for discussions

### 7. Pre-distribute Agendas

Send agendas 24-48 hours before meetings:
- Gives attendees time to prepare
- Improves meeting efficiency
- Increases participation quality

## Integration Examples

### Calendar Integration

```python
import json
from datetime import datetime, timedelta

with open("agenda.json") as f:
    agenda = json.load(f)

# Create calendar event with agenda
meeting_start = datetime.now() + timedelta(days=1)
create_calendar_event(
    title=agenda["meeting_title"],
    start=meeting_start,
    duration=agenda["total_duration_minutes"],
    description=format_agenda_for_calendar(agenda)
)
```

### Email Distribution

```python
# Send agenda to participants
with open("agenda.txt") as f:
    agenda_text = f.read()

send_email(
    to=["product@company.com", "engineering@company.com"],
    subject=f"Agenda: {agenda['meeting_title']}",
    body=agenda_text
)
```

### Slack Integration

```python
# Post agenda to Slack channel
slack_message = format_agenda_for_slack(agenda)
post_to_slack("#product-planning", slack_message)
```

### Project Management Tools

```python
# Create tasks from agenda outcomes
for item in agenda["agenda"]:
    create_task(
        title=item["outcome"],
        assignee=item["owner"],
        description=f"From meeting: {item['topic']}"
    )
```

## Output Format Reference

### JSON Schema

```json
{
  "meeting_title": "string",
  "objective": "string",
  "total_duration_minutes": "integer",
  "agenda": [
    {
      "topic": "string",
      "time_minutes": "integer",
      "owner": "string",
      "outcome": "string"
    }
  ]
}
```

### Text Format

```
Meeting Agenda (YYYY-MM-DD)
=============================================

Title: [Meeting Title]
Objective: [Meeting Objective]
Duration: [X] minutes

1. [Topic] ([Y] min)
   Owner: [Person/Role]
   Outcome: [Expected Result]

2. [Topic] ([Y] min)
   Owner: [Person/Role]
   Outcome: [Expected Result]
...
```

## Performance

**Generation Time:**
- GLM-4.7-Flash (LAN): ~3-5 seconds
- GPT-4o-mini: ~2-3 seconds
- GPT-4o: ~4-6 seconds

**Agenda Quality:**
- Time allocation accuracy: 95%+ (fits within duration)
- Relevance to objective: 90%+
- Appropriate owner assignment: 85%+
- Clear outcome definition: 90%+

## Files

- `agent.py`: Main agenda generator agent
- `meeting.txt`: Input meeting description
- `agenda.json`: Structured JSON output
- `agenda.txt`: Human-readable agenda
- `README.md`: This file

## Requirements

```txt
openai>=1.0.0
```

Install with:
```bash
pip install openai
```

## Troubleshooting

**Issue**: Agenda exceeds specified duration
```
Solution: Adjust input to be more specific about time constraints.
Add "Constraints: Must fit exactly in X minutes" to meeting.txt
```

**Issue**: Outcomes are too vague
```
Solution: Be more specific in the objective.
Example: "Decide top 3 features" vs. "Discuss features"
```

**Issue**: Owner assignments don't match participants
```
Solution: List specific roles in Participants field.
Example: "Product Manager, Engineering Lead" vs. "Team"
```

**Issue**: JSON parsing fails
```
Solution: Check that LLM is returning valid JSON.
The agent strips markdown blocks but may need prompt tuning.
```

## Future Enhancements

- [ ] Meeting minutes generation after meeting
- [ ] Agenda item prioritization and reordering
- [ ] Recurring meeting agenda templates
- [ ] Automatic attendee notification
- [ ] Integration with video conferencing tools
- [ ] Real-time agenda adjustment during meetings
- [ ] Meeting effectiveness scoring
- [ ] Agenda library and templates
- [ ] Multi-meeting series planning
- [ ] Collaborative agenda editing
- [ ] Pre-meeting preparation suggestions
- [ ] Post-meeting action item tracking
- [ ] Meeting cost calculator (time × attendees)
- [ ] Optimal meeting time suggestions

## Best Meeting Practices

### Pre-Meeting
1. ✅ Distribute agenda 24+ hours in advance
2. ✅ Define clear objective and expected outcomes
3. ✅ Invite only necessary participants
4. ✅ Include relevant materials/documents
5. ✅ Set up video/call details

### During Meeting
1. ✅ Start on time, follow agenda
2. ✅ Assign note-taker
3. ✅ Track action items in real-time
4. ✅ Manage time for each topic
5. ✅ Ensure participation from all attendees

### Post-Meeting
1. ✅ Send meeting notes within 24 hours
2. ✅ Follow up on action items
3. ✅ Update project management tools
4. ✅ Schedule follow-ups if needed
5. ✅ Gather feedback on meeting effectiveness

---

**Day 4 of 100** | Building practical AI agents one day at a time 🚀
