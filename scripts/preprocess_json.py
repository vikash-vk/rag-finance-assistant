import os
import json
import requests
import pandas as pd
import joblib

# =========================
# BASE PATH
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FOLDER = os.path.join(BASE_DIR, "data", "jsons_merged")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "embeddings.joblib")

EMBED_URL = "http://localhost:11434/api/embed"
MODEL = "bge-m3"

# =========================
# EMBEDDING FUNCTION
# =========================
def create_embedding(text_list):
    try:
        response = requests.post(
            EMBED_URL,
            json={
                "model": MODEL,
                "input": text_list
            }
        )
        return response.json()["embeddings"]
    except Exception as e:
        print("Embedding error:", e)
        return []

# =========================
# MAIN PROCESS
# =========================
def process_jsons(folder):
    all_data = []
    chunk_id = 0

    files = [f for f in os.listdir(folder) if f.endswith(".json")]

    for file in files:
        path = os.path.join(folder, file)

        with open(path, "r", encoding="utf-8") as f:
            content = json.load(f)

        chunks = content.get("chunks", [])
        texts = [c["text"] for c in chunks]

        embeddings = create_embedding(texts)

        for i, chunk in enumerate(chunks):
            chunk_data = {
                "chunk_id": chunk_id,
                "number": chunk.get("number"),
                "title": chunk.get("title"),
                "start": chunk.get("start"),
                "end": chunk.get("end"),
                "text": chunk.get("text"),
                "embedding": embeddings[i] if i < len(embeddings) else None
            }

            all_data.append(chunk_data)
            chunk_id += 1

    return all_data

# =========================
# RUN
# =========================
data = process_jsons(INPUT_FOLDER)
df = pd.DataFrame.from_records(data)

joblib.dump(df, OUTPUT_FILE)
print(f"Saved embeddings to {OUTPUT_FILE}")