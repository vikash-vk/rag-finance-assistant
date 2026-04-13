import os
import subprocess

# =========================
# BASE PATH
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VIDEOS_DIR = os.path.join(BASE_DIR, "videos")
AUDIOS_DIR = os.path.join(BASE_DIR, "audios")

# create audios folder if not exists
os.makedirs(AUDIOS_DIR, exist_ok=True)

# =========================
# Converts the videos to mp3
# =========================
files = os.listdir(VIDEOS_DIR)

for file in files:
    episode_number = file.split("- ")[1].split(".")[0]
    file_name = file.split(" | ")[0]

    print(episode_number, file_name)

    input_path = os.path.join(VIDEOS_DIR, file)
    output_path = os.path.join(AUDIOS_DIR, f"{episode_number}_{file_name}.mp3")

    subprocess.run(["ffmpeg", "-i", input_path, output_path])