# heygen6.py
# Generate HeyGen video by randomly selecting one script from a JSON file

import requests
import os
import time
import argparse
import random
import json
from dotenv import load_dotenv

load_dotenv()

# List of available avatar image_keys (randomly selected)
IMAGE_KEYS = [
    "image/1fbe4b94048145f5a80250eafd956ae1/original.png",
]

# Voice is Tranquil Tim
def generate_video(script, title="My Viral Reel", voice_id="6e05e310c3f14ed4ba1545578ce82ff6", image_key=None):
    selected_image_key = image_key or random.choice(IMAGE_KEYS)
    url = "https://api.heygen.com/v2/video/av4/generate"
    payload = {
        "video_orientation": "portrait",
        "image_key": selected_image_key,
        "video_title": title,
        "custom_motion_prompt": "Avatar maintains a serious and neutral facial expression with no smiling, occasional subtle hand gestures to emphasize points, slight head nods, and natural blinks while speaking.",
        "script": script,
        "voice_id": voice_id,
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "x-api-key": os.getenv('HEYGEN_API_KEY')
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("error") is None:
            video_id = data["data"]["video_id"]
            print(f"Success: Generation started → {video_id}")
            print(f"Using avatar → {selected_image_key}")
            return video_id
    print("Error:", response.text)
    return None

def check_status(video_id):
    url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
    headers = {"x-api-key": os.getenv('HEYGEN_API_KEY')}
    for _ in range(50):
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            data = r.json()
            if data.get("code") == 100:
                status = data["data"]["status"]
                print(f"Status: {status}")
                if status == "completed":
                    return data["data"]["video_url"]
        time.sleep(60)
    return None

def download(video_url, video_id):
    os.makedirs("media", exist_ok=True)
    path = f"media/{video_id}.mp4"
    print(f"Downloading → {path}")
    r = requests.get(video_url, stream=True)
    if r.status_code == 200:
        with open(path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        print(f"Downloaded: {path}")
        return path
    return None

def main():
    parser = argparse.ArgumentParser(description="Generate HeyGen video by randomly picking one script from a JSON file")
    parser.add_argument("--json", type=str, required=True,
                        help="Path to JSON file containing an array of script objects")
    parser.add_argument("--title", type=str, default="My Viral Reel", help="Override video title")
    parser.add_argument("--voice", type=str, default="6e05e310c3f14ed4ba1545578ce82ff6", help="Override voice ID")
    args = parser.parse_args()

    # Load and validate JSON file
    if not os.path.exists(args.json):
        print(f"JSON file not found: {args.json}")
        return

    try:
        with open(args.json, "r", encoding="utf-8") as f:
            scripts_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in file: {e}")
        return

    if not isinstance(scripts_data, list) or len(scripts_data) == 0:
        print("JSON must contain a non-empty array of script objects")
        return

    # Randomly select one script entry
    selected_entry = random.choice(scripts_data)

    if "script" not in selected_entry:
        print("Selected entry is missing 'script' field")
        return

    script_text = selected_entry["script"].strip()
    niche = selected_entry.get("niche", "unknown_niche")

    if not script_text:
        print("Selected script is empty!")
        return

    print(f"Loaded {len(scripts_data)} scripts from {args.json}")
    print(f"Randomly selected script (niche: {niche})")
    print("-" * 50)
    print(script_text)
    print("-" * 50)

    # Generate video
    video_id = generate_video(
        script=script_text,
        title=args.title,
        voice_id=args.voice
    )
    if not video_id:
        return

    print("Waiting for render (this can take 5-15 minutes)...")
    video_url = check_status(video_id)
    if not video_url:
        print("Timed out waiting for video completion")
        return

    output_path = download(video_url, video_id)
    if output_path:
        print(f"\nHEYGEN VIDEO READY")
        print(f"OUTPUT_PATH={output_path}")

if __name__ == "__main__":
    main()