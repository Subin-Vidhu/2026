import json
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from datetime import date

# Using Ollama on LAN instead of OpenAI
client = OpenAI(
    base_url="http://192.168.0.18:11444/v1",
    api_key="ollama"  # Ollama doesn't require a real API key
)

# Load embedding model (cached after first download)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
CHAT_MODEL = "glm-4.7-flash:latest"


# def read_notes(path="notes.txt"):
def read_notes(path="profile.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def embed_texts(texts):
    """Generate semantic embeddings using Sentence-Transformers"""
    # Returns embeddings as list of lists (compatible with cosine_similarity)
    embeddings = embedding_model.encode(texts, convert_to_tensor=False)
    return embeddings.tolist()
def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
 
 
def store_knowledge(chunks, embeddings):
    records = []
    for text, emb in zip(chunks, embeddings):
        records.append({
            "text": text,
            "embedding": emb,
            "created": date.today().isoformat()
        })
    with open("knowledge.json", "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
    return records
 
 
def load_knowledge():
    with open("knowledge.json", "r", encoding="utf-8") as f:
        return json.load(f)
 
 
def retrieve(query, records, top_k=3):
    query_emb = embed_texts([query])[0]
    scored = []
    for r in records:
        score = cosine_similarity(query_emb, r["embedding"])
        scored.append((score, r["text"]))
    scored.sort(reverse=True)
    return [text for _, text in scored[:top_k]]
 
 
def answer_query(query, contexts):
    prompt = f"""
Answer the following question using ONLY the provided notes.
 
Notes:
{chr(10).join(contexts)}
 
Question:
{query}
"""
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content
 
 
def main():
    print("Ingesting notes...")
    chunks = read_notes()
    embeddings = embed_texts(chunks)
    records = store_knowledge(chunks, embeddings)
 
    print("Knowledge base ready.")
    query = input("\nAsk a question: ")
    top_contexts = retrieve(query, records)
    answer = answer_query(query, top_contexts)
 
    print("\nAnswer:")
    print(answer)
 
 
if __name__ == "__main__":
    main()