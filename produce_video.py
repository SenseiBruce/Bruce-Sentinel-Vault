import json
import os
import sys
import asyncio
import time
import argparse
from uuid import uuid4
import requests

# Add src to path so we can import classes
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from classes.YouTube import YouTube
from classes.Tts import TTS
from runware import Runware, IImageInference
from config import get_model, get_image_prompt_llm

# Configuration
RUNWARE_API_KEY = "MZewvUENNGcoAdkQr5tt3Xxr4J96DxcJ"
SCRIPTS_FILE = "/Users/kinshuk.prasad/Downloads/NLP scripts.json"
MATON_KEY = "OR3M7YdqmfSxvcRWKwlJ0rPUkf0SOSjilQkHY_EGXhDV0kgRVtqrqDOR4wCYXlP4gaGazWUECzsuoyjaekaWhJTNR7067US1TelbYTHWfQ"

async def generate_images_with_runware(prompts, save_dir=None):
    """
    Generate images using Runware SDK (Async).
    """
    print(f"⚡ Runware: Connecting...")
    runware = Runware(api_key=RUNWARE_API_KEY)
    await runware.connect()

    request_image = IImageInference(
        positivePrompt=prompts[0],
        model="runware:100@1",
        numberResults=1,
        height=1920,
        width=1088
    )
    
    generated_paths = []
    base_dir = save_dir if save_dir else os.path.join(os.path.dirname(__file__), ".mp")
    
    for i, prompt in enumerate(prompts):
        print(f"⚡ Runware: Generating Image {i+1}/{len(prompts)}...")
        request_image.positivePrompt = prompt
        
        try:
            images = await runware.imageInference(request_image)
            for image in images:
                response = requests.get(image.imageURL)
                if response.status_code == 200:
                    image_path = os.path.join(base_dir, f"img_{i:02d}_{uuid4()}.png")
                    with open(image_path, "wb") as f:
                        f.write(response.content)
                    generated_paths.append(image_path)
        except Exception as e:
            print(f"   ❌ Runware Error: {e}")

    return generated_paths

def upload_to_drive(file_path):
    if not os.path.exists(file_path): return
    filename = os.path.basename(file_path)
    print(f"🚀 Uploading {filename} to Drive...")
    headers = {"Authorization": f"Bearer {MATON_KEY}"}
    url = "https://gateway.maton.ai/google-drive/upload/drive/v3/files?uploadType=multipart"
    metadata = {"name": filename, "mimeType": "video/mp4"}
    
    try:
        files = {
            'data': ('metadata', json.dumps(metadata), 'application/json'),
            'file': (filename, open(file_path, 'rb'), 'video/mp4')
        }
        response = requests.post(url, headers=headers, files=files)
        if response.status_code == 200:
            print(f"✅ Drive Upload Success! ID: {response.json().get('id')}")
        else:
            print(f"❌ Drive Upload Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Upload Error: {e}")

class VideoFactory:
    def __init__(self, scripts_file):
        self.scripts_file = scripts_file
        self.scripts = self._load_scripts()
        self.tts = TTS()

    def _load_scripts(self):
        if not os.path.exists(self.scripts_file):
            print(f"❌ Script file not found: {self.scripts_file}")
            sys.exit(1)
        with open(self.scripts_file, "r") as f:
            return json.load(f)

    def produce(self, index):
        if index < 1 or index > len(self.scripts):
            print(f"❌ Invalid index: {index}. Range: 1-{len(self.scripts)}")
            return

        entry = self.scripts[index - 1]
        topic = entry.get("project_name", f"Video_{index}")
        scenes = entry.get("scenes", [])
        
        print(f"\n🎬 [VideoFactory] Building: {topic}")
        
        # 1. Setup Environment
        youtube = YouTube(f"prod-{index}", "factory", "", topic, "English")
        video_slug = f"video_{index}_{topic.replace(' ', '_')[:30]}"
        video_dir = os.path.join(os.path.dirname(__file__), ".mp", video_slug)
        if not os.path.exists(video_dir): os.makedirs(video_dir)

        # 2. Image Generation
        prompts = [scene.get("image_prompt", "") for scene in scenes]
        existing_images = sorted([os.path.join(video_dir, f) for f in os.listdir(video_dir) if f.endswith(".png") and os.path.basename(f).startswith("img_")])
        
        if len(existing_images) >= len(prompts):
            print(f"♻️ Reusing {len(existing_images)} cached images.")
            generated_images = existing_images[:len(prompts)]
        else:
            generated_images = asyncio.run(generate_images_with_runware(prompts, save_dir=video_dir))

        if len(generated_images) < len(scenes):
            print("❌ Critical: Image generation failed or incomplete.")
            return

        # 3. Scene Processing
        scene_clips = []
        for i, scene in enumerate(scenes):
            print(f"🎥 Rendering Scene {i+1}/{len(scenes)}...")
            clip = youtube.process_scene(scene, self.tts, generated_images[i])
            if clip: scene_clips.append(clip)

        # 4. Final Assembly
        if scene_clips:
            print("🎞️ Stitching Final Video...")
            final_path = youtube.combine_scenes(scene_clips)
            if final_path:
                new_name = os.path.join(os.path.dirname(final_path), f"FINAL_{index}_{topic.replace(' ', '_')[:30]}.mp4")
                os.rename(final_path, new_name)
                upload_to_drive(new_name)
                print(f"✨ Production Complete: {new_name}")
        else:
            print("❌ No scenes processed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Professional Video Production Factory")
    parser.add_argument("--index", type=int, required=True, help="Script index (1-based)")
    parser.add_argument("--file", type=str, default=SCRIPTS_FILE, help="Scripts JSON path")
    args = parser.parse_args()

    factory = VideoFactory(args.file)
    factory.produce(args.index)
