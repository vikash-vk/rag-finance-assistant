import whisper
import json
import os

# =========================
# BASE PATH
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AUDIOS_DIR = os.path.join(BASE_DIR, "audios")
JSONS_DIR = os.path.join(BASE_DIR, "jsons")

# create jsons folder if not exists
os.makedirs(JSONS_DIR, exist_ok=True)

# =========================
# Converts mp3 to json
# =========================
model = whisper.load_model("small.en")

audios = os.listdir(AUDIOS_DIR)

for audio in audios:
    if "_" in audio:

        number = audio.split("_")[0]
        title = audio.split("_")[1][:-4]

        audio_path = os.path.join(AUDIOS_DIR, audio)

        result = model.transcribe(audio=audio_path, word_timestamps=False)

        chunks = []
        for segment in result["segments"]:
            chunks.append({
                "number": number,
                "title": title,
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            })

        chunks_with_metadata = {
            "chunks": chunks,
            "text": result["text"]
        }

        output_path = os.path.join(JSONS_DIR, f"{audio}.json")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(chunks_with_metadata, f, indent=4)