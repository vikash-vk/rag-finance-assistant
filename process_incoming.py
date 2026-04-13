import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import requests
import joblib

# =========================
# BASE PATH
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "embeddings.joblib")

# =========================
# CONFIG
# =========================
EMBED_URL = "http://localhost:11434/api/embed"
GEN_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

# =========================
# EMBEDDING FUNCTION
# =========================
def create_embedding(text_list):
    try:
        r = requests.post(EMBED_URL, json={
            "model": "bge-m3",
            "input": text_list
        })
        return r.json()["embeddings"]
    except Exception as e:
        print("Embedding error:", e)
        return None

# =========================
# LLM INFERENCE
# =========================
def inference_ollama(prompt):
    try:
        r = requests.post(
            GEN_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False,
                "temperature": 0.3,
                "num_predict": 80
            }
        )
        return r.json()["response"]

    except Exception as e:
        print("Generation error:", e)
        return ""

# =========================
# LOAD DATA
# =========================
df = joblib.load(DATA_PATH)

# =========================
# HELPER FUNCTION
# =========================
def sec_to_min_sec(seconds):
    seconds = int(seconds)
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes}:{secs:02d}"

# =========================
# MAIN FUNCTION
# =========================
def answer_query(query):

    embeddings = create_embedding([query])
    if embeddings is None:
        return "Embedding failed", None

    query_embedding = embeddings[0]

    similarities = cosine_similarity(
        np.vstack(df["embedding"]),
        [query_embedding]
    ).flatten()

    top_k = 3
    top_indices = similarities.argsort()[::-1][:top_k]
    top_chunks = df.iloc[top_indices]

    context = "\n".join(
        f"Video {row['number']} - {row['title']} "
        f"({sec_to_min_sec(row['start'])}-{sec_to_min_sec(row['end'])}): {row['text']}"
        for _, row in top_chunks.iterrows()
    )

    # =========================
    # PROMPT (UNCHANGED)
    # =========================
    prompt = f'''
You are a helpful and friendly teaching assistant for the Zerodha Varsity course:
"Personal Finance for Beginners".
Your job is to help beginners understand financial concepts using the provided video transcript excerpts.
-----------------------
CONTEXT (from course videos):
{context}
-----------------------
USER QUESTION:
{query}
-----------------------
INSTRUCTIONS:
1. Answer ONLY using the given context.
2. Explain in a simple and beginner-friendly way.
3. Clearly mention:
   - Video number
   - Video title
   - Approximate timestamp (start-end seconds)
4. Guide the user on where to watch in the video.
5. If multiple parts are relevant, combine them naturally.
6. Keep the answer:
   - clear
   - concise
   - helpful
7. If the answer is not found in the context, say:
   "I can only answer questions related to the Zerodha Varsity Personal Finance course."
8. DO NOT mention:
   - JSON
   - chunks
   - technical details
9. Speak like a mentor teaching a beginner.
-----------------------
ANSWER:
'''

    # =========================
    # GET RESPONSE
    # =========================
    response = inference_ollama(prompt)
    return response, top_chunks