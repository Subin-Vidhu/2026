import json
from datetime import date
from openai import OpenAI
 
# Using Ollama on LAN instead of OpenAI
client = OpenAI(
    base_url="http://192.168.0.18:11444/v1",
    api_key="ollama"  # Ollama doesn't require a real API key
)
 
SYSTEM_PROMPT = """
You are an Email Summarization Agent.
 
Your job:
1. Summarize the email in 2–3 sentences
2. Extract key points
3. Extract action items (who should do what)
4. Identify deadlines
5. Classify urgency: Low, Medium, or High
 
Return ONLY valid JSON with this schema:
 
{
  "summary": "",
  "key_points": [],
  "action_items": [],
  "deadlines": [],
  "urgency": ""
}
"""
 
def read_email(path="email.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
 
def summarize_email(email_text):
    response = client.chat.completions.create(
        model="glm-4.7-flash:latest",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": email_text}
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
    with open("summary.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
 
    with open("summary.txt", "w", encoding="utf-8") as f:
        f.write(f"Email Summary ({date.today()})\n")
        f.write("=" * 40 + "\n\n")
        f.write("SUMMARY:\n")
        f.write(data["summary"] + "\n\n")
 
        f.write("KEY POINTS:\n")
        for p in data["key_points"]:
            f.write(f"- {p}\n")
 
        f.write("\nACTION ITEMS:\n")
        for a in data["action_items"]:
            f.write(f"- {a}\n")
 
        f.write("\nDEADLINES:\n")
        for d in data["deadlines"]:
            f.write(f"- {d}\n")
 
        f.write(f"\nURGENCY: {data['urgency']}\n")
 
def main():
    email_text = read_email()
    result = summarize_email(email_text)
    save_outputs(result)
    print("Email summarized successfully.")
    print(result)
 
if __name__ == "__main__":
    main()