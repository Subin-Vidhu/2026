import json
from datetime import date
from urllib import response
from openai import OpenAI
 
# Using Ollama on LAN instead of OpenAI
client = OpenAI(
    base_url="http://192.168.0.18:11444/v1",
    api_key="ollama"  # Ollama doesn't require a real API key
)
 
SYSTEM_PROMPT = """
You are a Meeting Agenda Generator Agent.
 
Your job is to generate a clear, time-boxed meeting agenda.
 
Rules:
- Agenda must fit within the provided duration
- Focus on the meeting objective
- Include time allocation for each item
- Identify decision points where applicable
- Return ONLY valid JSON with this schema:
 
{
  "meeting_title": "",
  "objective": "",
  "total_duration_minutes": 0,
  "agenda": [
    {
      "topic": "",
      "time_minutes": 0,
      "owner": "",
      "outcome": ""
    }
  ]
}
"""
 
def read_input(path="meeting.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
 
def generate_agenda(meeting_text):
    response = client.chat.completions.create(
        model="glm-4.7-flash:latest",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": meeting_text}
        ],
        temperature=0.2
    )
    
    content = response.choices[0].message.content
    
    # Handle markdown code blocks
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON. Raw response:\n{content}\n")
        raise e
 
def save_outputs(data):
    with open("agenda.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
 
    with open("agenda.txt", "w", encoding="utf-8") as f:
        f.write(f"Meeting Agenda ({date.today()})\n")
        f.write("=" * 45 + "\n\n")
        f.write(f"Title: {data['meeting_title']}\n")
        f.write(f"Objective: {data['objective']}\n")
        f.write(f"Duration: {data['total_duration_minutes']} minutes\n\n")
 
        for i, item in enumerate(data["agenda"], 1):
            f.write(f"{i}. {item['topic']} ({item['time_minutes']} min)\n")
            f.write(f"   Owner: {item['owner']}\n")
            f.write(f"   Outcome: {item['outcome']}\n\n")
 
def main():
    meeting_text = read_input()
    agenda = generate_agenda(meeting_text)
    save_outputs(agenda)
    print("Meeting agenda generated successfully.")
    print(agenda)
 
if __name__ == "__main__":
    main()