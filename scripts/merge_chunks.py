import os
import json

# =========================
# BASE PATH
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FOLDER = os.path.join(BASE_DIR, "jsons")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "jsons_merged")

GROUP_SIZE = 5

# Create output folder if not exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# =========================
# MERGE FUNCTION
# =========================
def merge_chunks(chunks, group_size):
    merged = []

    for i in range(0, len(chunks), group_size):
        group = chunks[i:i + group_size]

        if not group:
            continue

        merged_chunk = {
            "number": group[0].get("number"),
            "title": group[0].get("title"),
            "start": group[0].get("start"),
            "end": group[-1].get("end"),
            "text": " ".join(c.get("text", "") for c in group)
        }

        merged.append(merged_chunk)

    return merged

# =========================
# PROCESS FILES
# =========================
def process_files(input_folder, output_folder):
    files = [f for f in os.listdir(input_folder) if f.endswith(".json")]

    for file in files:
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file)

        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        chunks = data.get("chunks", [])

        merged_chunks = merge_chunks(chunks, GROUP_SIZE)

        output_data = {
            "chunks": merged_chunks,
            "text": data.get("text", "")
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4)

    print("Merged JSONs created successfully!")

# =========================
# RUN
# =========================
process_files(INPUT_FOLDER, OUTPUT_FOLDER)