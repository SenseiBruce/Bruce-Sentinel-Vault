"""Video production factory: scripts JSON -> images -> scenes -> Drive upload."""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from uuid import uuid4

import requests

from sentinel_logging import configure_logging

logger = logging.getLogger(__name__)

# Prefer local schemas package when running from repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent / "grader-agent" / "src"))
try:
    from schemas import SchemaError, parse_script_entries
except ImportError:  # pragma: no cover
    SchemaError = ValueError  # type: ignore[misc, assignment]
    parse_script_entries = None  # type: ignore[assignment]

# Optional local multimedia helpers (may be absent in minimal installs).
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
try:
    from classes.Tts import TTS
    from classes.YouTube import YouTube
except ImportError:  # pragma: no cover - exercised only when helpers are missing
    YouTube = None
    TTS = None

try:
    from runware import IImageInference, Runware
except ImportError:  # pragma: no cover
    Runware = None
    IImageInference = None


class ConfigurationError(RuntimeError):
    """Raised when required configuration is missing or invalid."""


class ProductionError(RuntimeError):
    """Raised when a production step fails in a non-recoverable way."""


def _require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ConfigurationError(
            f"Missing required environment variable: {name}. "
            f"Copy .env.example to .env and set {name}."
        )
    return value


def default_scripts_file() -> str:
    return os.environ.get(
        "SCRIPTS_FILE",
        str(Path(__file__).resolve().parent / "scripts.example.json"),
    )


async def generate_images_with_runware(prompts, save_dir=None, api_key=None):
    """Generate images using Runware SDK (async)."""
    if Runware is None or IImageInference is None:
        raise ProductionError(
            "runware package is not installed. pip install -r requirements.txt"
        )

    key = api_key or _require_env("RUNWARE_API_KEY")
    logger.info("Runware: connecting")
    runware = Runware(api_key=key)
    await runware.connect()

    request_image = IImageInference(
        positivePrompt=prompts[0] if prompts else "",
        model="runware:100@1",
        numberResults=1,
        height=1920,
        width=1088,
    )

    generated_paths = []
    base_dir = save_dir if save_dir else os.path.join(os.path.dirname(__file__), ".mp")
    os.makedirs(base_dir, exist_ok=True)

    for i, prompt in enumerate(prompts):
        logger.info("Runware: generating image %s/%s", i + 1, len(prompts))
        request_image.positivePrompt = prompt
        try:
            images = await runware.imageInference(request_image)
            for image in images:
                response = requests.get(image.imageURL, timeout=60)
                response.raise_for_status()
                image_path = os.path.join(base_dir, f"img_{i:02d}_{uuid4()}.png")
                with open(image_path, "wb") as handle:
                    handle.write(response.content)
                generated_paths.append(image_path)
        except Exception:
            logger.exception("Runware image generation failed for prompt index %s", i)

    return generated_paths


def upload_to_drive(file_path, maton_key=None):
    """Upload a finished video to Google Drive via the Maton gateway."""
    if not os.path.exists(file_path):
        raise ProductionError(f"Upload target does not exist: {file_path}")

    filename = os.path.basename(file_path)
    key = maton_key or _require_env("MATON_KEY")
    logger.info("Uploading %s to Drive", filename)
    headers = {"Authorization": f"Bearer {key}"}
    url = (
        "https://gateway.maton.ai/google-drive/upload/drive/v3/files"
        "?uploadType=multipart"
    )
    metadata = {"name": filename, "mimeType": "video/mp4"}

    try:
        with open(file_path, "rb") as media:
            files = {
                "data": ("metadata", json.dumps(metadata), "application/json"),
                "file": (filename, media, "video/mp4"),
            }
            response = requests.post(url, headers=headers, files=files, timeout=120)
        if response.status_code == 200:
            logger.info("Drive upload success id=%s", response.json().get("id"))
            return response.json()
        raise ProductionError(
            f"Drive upload failed: HTTP {response.status_code}: {response.text[:200]}"
        )
    except ProductionError:
        raise
    except Exception as exc:
        logger.exception("Drive upload error")
        raise ProductionError(f"Drive upload error: {exc}") from exc


class VideoFactory:
    def __init__(self, scripts_file, tts=None, youtube_factory=None):
        self.scripts_file = scripts_file
        self.scripts = self._load_scripts()
        if tts is not None:
            self.tts = tts
        elif TTS is not None:
            self.tts = TTS()
        else:
            self.tts = None
        self._youtube_factory = youtube_factory

    def _load_scripts(self):
        if not os.path.exists(self.scripts_file):
            raise ConfigurationError(f"Script file not found: {self.scripts_file}")
        with open(self.scripts_file, encoding="utf-8") as handle:
            raw = json.load(handle)
        if parse_script_entries is None:
            if not isinstance(raw, list):
                raise ConfigurationError("scripts JSON must be a list")
            return raw
        try:
            entries = parse_script_entries(raw)
        except SchemaError as exc:
            raise ConfigurationError(f"Invalid scripts JSON: {exc}") from exc
        return [entry.model_dump() for entry in entries]

    def _build_youtube(self, index, topic):
        if self._youtube_factory is not None:
            return self._youtube_factory(index, topic)
        if YouTube is None:
            raise ProductionError(
                "YouTube/TTS helpers are not available. Install project multimedia "
                "dependencies under src/classes/."
            )
        return YouTube(f"prod-{index}", "factory", "", topic, "English")

    def produce(self, index):
        if index < 1 or index > len(self.scripts):
            raise ConfigurationError(
                f"Invalid index: {index}. Range: 1-{len(self.scripts)}"
            )

        entry = self.scripts[index - 1]
        topic = entry.get("project_name", f"Video_{index}")
        scenes = entry.get("scenes", [])

        logger.info("[VideoFactory] Building: %s", topic)

        youtube = self._build_youtube(index, topic)
        video_slug = f"video_{index}_{topic.replace(' ', '_')[:30]}"
        video_dir = os.path.join(os.path.dirname(__file__), ".mp", video_slug)
        os.makedirs(video_dir, exist_ok=True)

        prompts = [scene.get("image_prompt", "") for scene in scenes]
        existing_images = sorted(
            [
                os.path.join(video_dir, name)
                for name in os.listdir(video_dir)
                if name.endswith(".png") and name.startswith("img_")
            ]
        )

        if len(existing_images) >= len(prompts):
            logger.info("Reusing %s cached images", len(existing_images))
            generated_images = existing_images[: len(prompts)]
        else:
            generated_images = asyncio.run(
                generate_images_with_runware(prompts, save_dir=video_dir)
            )

        if len(generated_images) < len(scenes):
            raise ProductionError("Image generation failed or incomplete.")

        scene_clips = []
        for i, scene in enumerate(scenes):
            logger.info("Rendering scene %s/%s", i + 1, len(scenes))
            clip = youtube.process_scene(scene, self.tts, generated_images[i])
            if clip:
                scene_clips.append(clip)

        if not scene_clips:
            raise ProductionError("No scenes processed successfully.")

        logger.info("Stitching final video")
        final_path = youtube.combine_scenes(scene_clips)
        if not final_path:
            raise ProductionError("combine_scenes returned no path")

        new_name = os.path.join(
            os.path.dirname(final_path),
            f"FINAL_{index}_{topic.replace(' ', '_')[:30]}.mp4",
        )
        os.rename(final_path, new_name)
        upload_to_drive(new_name)
        logger.info("Production complete: %s", new_name)
        return new_name


def main(argv=None):
    configure_logging()
    parser = argparse.ArgumentParser(description="Professional Video Production Factory")
    parser.add_argument("--index", type=int, required=True, help="Script index (1-based)")
    parser.add_argument(
        "--file",
        type=str,
        default=default_scripts_file(),
        help="Scripts JSON path (default: SCRIPTS_FILE or ./scripts.example.json)",
    )
    args = parser.parse_args(argv)

    factory = VideoFactory(args.file)
    factory.produce(args.index)


if __name__ == "__main__":
    main()
