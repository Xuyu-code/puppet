"""Configuration for the public portfolio application."""

from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
WEBAPP_ROOT = PROJECT_ROOT / "webapp"
DATA_DIR = WEBAPP_ROOT / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
RESULTS_DIR = DATA_DIR / "results"
DB_PATH = DATA_DIR / "app.db"

PROVIDER_MODE = os.environ.get("PUPPET_PROVIDER_MODE", "mock").strip().lower()
PROVIDER_URL = os.environ.get("PUPPET_GENERATION_API_URL", "").strip()
PROVIDER_API_KEY = os.environ.get("PUPPET_GENERATION_API_KEY", "").strip()
PROVIDER_TIMEOUT_SECONDS = float(os.environ.get("PUPPET_GENERATION_TIMEOUT_SECONDS", "180"))

DEFAULT_CANDIDATE_COUNT = 3
DEFAULT_STEPS = 40
DEFAULT_GUIDANCE_SCALE = 8.0
DEFAULT_CONDITIONING_SCALE = 0.5
DEFAULT_SIMPLE_WEIGHT = 0.4
DEFAULT_COMPLEX_WEIGHT = 0.6
DEFAULT_SEED = 42
DEFAULT_POSTPROCESS = True

MAX_UPLOAD_BYTES = 5 * 1024 * 1024
ALLOWED_IMAGE_FORMATS = {"PNG", "JPEG", "WEBP", "BMP"}

RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMITED_PATHS = {"/api/generate"}

CORS_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:4173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:4173",
]

PRESET_PROMPTS = [
    {
        "name": "左向旦角 · 玄黑仪冠",
        "prompt": "Hehuang shadow puppet portrait, left-facing female role, black ceremonial crown, intricate leather carving, pure white background",
    },
    {
        "name": "右向生角 · 朱红王帽",
        "prompt": "Hehuang shadow puppet portrait, right-facing male role, vermilion traditional crown, balanced carved ornaments, pure white background",
    },
    {
        "name": "正向神怪 · 琥珀纹样",
        "prompt": "Hehuang shadow puppet portrait, frontal mythical character, amber and black palette, bold folk ornament, pure white background",
    },
]

HOST = os.environ.get("WEBAPP_HOST", "0.0.0.0")
PORT = int(os.environ.get("WEBAPP_PORT", "8000"))


def ensure_data_dirs() -> None:
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
