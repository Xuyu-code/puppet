"""FastAPI backend for the Hehuang shadow-puppet portfolio application."""

from __future__ import annotations

import io
import re
import time
import uuid
from collections import deque
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, Query, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from PIL import Image

from . import db
from .config import (
    ALLOWED_IMAGE_FORMATS,
    CORS_ORIGINS,
    DEFAULT_CANDIDATE_COUNT,
    DEFAULT_COMPLEX_WEIGHT,
    DEFAULT_CONDITIONING_SCALE,
    DEFAULT_GUIDANCE_SCALE,
    DEFAULT_POSTPROCESS,
    DEFAULT_SEED,
    DEFAULT_SIMPLE_WEIGHT,
    DEFAULT_STEPS,
    HOST,
    MAX_UPLOAD_BYTES,
    PORT,
    PRESET_PROMPTS,
    RATE_LIMITED_PATHS,
    RATE_LIMIT_REQUESTS,
    RATE_LIMIT_WINDOW_SECONDS,
    RESULTS_DIR,
    UPLOADS_DIR,
    ensure_data_dirs,
)
from .provider import get_provider
from .schemas import (
    GenerateResponse,
    HealthResponse,
    HistoryDetailResponse,
    HistoryItem,
    HistoryListResponse,
    Preset,
    PresetListResponse,
    TaskResult,
    TaskStatusResponse,
    TranslateRequest,
    TranslateResponse,
    normalize_candidate_score,
)
from .tasks import task_queue

_IMAGE_NAME_RE = re.compile(r"^(candidate_\d+|selected|final|condition_simple|condition_complex)\.png$")


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_data_dirs()
    db.init_db()
    task_queue.start()
    yield


app = FastAPI(title="Hehuang Shadow Puppet Platform API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_rate_buckets: dict[str, deque[float]] = {}


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if request.url.path in RATE_LIMITED_PATHS and request.method == "POST":
        client = request.client.host if request.client else "unknown"
        now = time.monotonic()
        bucket = _rate_buckets.setdefault(client, deque())
        while bucket and now - bucket[0] > RATE_LIMIT_WINDOW_SECONDS:
            bucket.popleft()
        if len(bucket) >= RATE_LIMIT_REQUESTS:
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded."})
        bucket.append(now)
    return await call_next(request)


def _validate_lineart(data: bytes, filename: str) -> None:
    if not data:
        raise HTTPException(status_code=400, detail="Empty lineart file.")
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=400, detail="Lineart exceeds the 5MB limit.")
    try:
        with Image.open(io.BytesIO(data)) as image:
            image.verify()
            image_format = image.format
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"'{filename}' is not a valid image file.") from exc
    if image_format not in ALLOWED_IMAGE_FORMATS:
        raise HTTPException(status_code=400, detail=f"Unsupported image format '{image_format}'.")


def _result_from_db_row(row: dict) -> TaskResult | None:
    if row["status"] != "done" or not row["candidate_count"] or not row["candidate_scores_json"]:
        return None
    import json

    task_id = row["id"]
    params = json.loads(row["params_json"] or "{}")
    scores = [normalize_candidate_score(item) for item in json.loads(row["candidate_scores_json"])]

    def url(filename: str) -> str:
        return f"/api/images/{task_id}/{filename}"

    return TaskResult(
        candidate_urls=[url(f"candidate_{index + 1}.png") for index in range(row["candidate_count"])],
        candidate_scores=scores,
        selected_index=row["selected_index"] or 0,
        selected_url=url("selected.png"),
        final_url=url("final.png"),
        condition_simple_url=url("condition_simple.png"),
        condition_complex_url=url("condition_complex.png"),
        elapsed_seconds=row["elapsed_seconds"],
        simple_mode=params.get("simple_mode", "auto"),
    )


@app.post("/api/generate", response_model=GenerateResponse)
async def generate(
    lineart: UploadFile = File(...),
    prompt: str = Form(...),
    negative_prompt: str | None = Form(None),
    candidate_count: int = Form(DEFAULT_CANDIDATE_COUNT),
    steps: int = Form(DEFAULT_STEPS),
    guidance_scale: float = Form(DEFAULT_GUIDANCE_SCALE),
    conditioning_scale: float = Form(DEFAULT_CONDITIONING_SCALE),
    simple_weight: float = Form(DEFAULT_SIMPLE_WEIGHT),
    complex_weight: float = Form(DEFAULT_COMPLEX_WEIGHT),
    seed: int = Form(DEFAULT_SEED),
    postprocess: bool = Form(DEFAULT_POSTPROCESS),
    simple_lineart: UploadFile | None = File(None),
):
    provider = get_provider()
    if not provider.ready:
        raise HTTPException(status_code=503, detail="The generation provider is not configured.")
    if not prompt.strip():
        raise HTTPException(status_code=400, detail="prompt must not be empty.")
    if not 1 <= candidate_count <= 8:
        raise HTTPException(status_code=400, detail="candidate_count must be between 1 and 8.")
    if not 1 <= steps <= 150:
        raise HTTPException(status_code=400, detail="steps must be between 1 and 150.")

    data = await lineart.read()
    _validate_lineart(data, lineart.filename or "lineart")
    task_id = uuid.uuid4().hex[:12]
    suffix = Path(lineart.filename or "lineart.png").suffix.lower() or ".png"
    upload_path = UPLOADS_DIR / f"{task_id}{suffix}"
    upload_path.write_bytes(data)

    simple_upload_path: Path | None = None
    if simple_lineart is not None:
        simple_data = await simple_lineart.read()
        _validate_lineart(simple_data, simple_lineart.filename or "simple_lineart")
        simple_suffix = Path(simple_lineart.filename or "simple.png").suffix.lower() or ".png"
        simple_upload_path = UPLOADS_DIR / f"{task_id}_simple{simple_suffix}"
        simple_upload_path.write_bytes(simple_data)

    params = {
        "candidate_count": candidate_count,
        "steps": steps,
        "guidance_scale": guidance_scale,
        "conditioning_scale": conditioning_scale,
        "simple_weight": simple_weight,
        "complex_weight": complex_weight,
        "seed": seed,
        "postprocess": postprocess,
        "simple_mode": "expert" if simple_upload_path is not None else "auto",
    }
    _, position = task_queue.enqueue(
        task_id=task_id,
        lineart_path=upload_path,
        prompt=prompt.strip(),
        negative_prompt=negative_prompt,
        params=params,
        simple_lineart_path=simple_upload_path,
    )
    return GenerateResponse(task_id=task_id, position=position)


@app.get("/api/tasks/{task_id}", response_model=TaskStatusResponse)
async def get_task(task_id: str):
    task = task_queue.get(task_id)
    if task is not None:
        return TaskStatusResponse(
            task_id=task.task_id,
            status=task.status,
            position=task_queue.position_of(task.task_id),
            created_at=task.created_at,
            error=task.error,
            result=TaskResult(**task.result) if task.result else None,
        )
    row = db.get_task(task_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Unknown task_id.")
    return TaskStatusResponse(
        task_id=task_id,
        status=row["status"],
        position=None,
        created_at=row["created_at"],
        error=row["error"],
        result=_result_from_db_row(row),
    )


@app.get("/api/history", response_model=HistoryListResponse)
async def history(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0)):
    total, rows = db.list_tasks(limit=limit, offset=offset)
    items = [
        HistoryItem(
            task_id=row["id"],
            created_at=row["created_at"],
            status=row["status"],
            prompt_preview=row["prompt"][:80] + ("..." if len(row["prompt"]) > 80 else ""),
            thumbnail_url=f"/api/images/{row['id']}/final.png" if row["status"] == "done" else None,
            elapsed_seconds=row["elapsed_seconds"],
        )
        for row in rows
    ]
    return HistoryListResponse(total=total, items=items)


@app.get("/api/history/{task_id}", response_model=HistoryDetailResponse)
async def history_detail(task_id: str):
    import json

    row = db.get_task(task_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Unknown task_id.")
    return HistoryDetailResponse(
        task_id=task_id,
        created_at=row["created_at"],
        status=row["status"],
        prompt=row["prompt"],
        negative_prompt=row["negative_prompt"],
        params=json.loads(row["params_json"] or "{}"),
        error=row["error"],
        result=_result_from_db_row(row),
    )


@app.get("/api/images/{task_id}/{filename}")
async def get_image(task_id: str, filename: str):
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", task_id) or not _IMAGE_NAME_RE.fullmatch(filename):
        raise HTTPException(status_code=404, detail="Not found.")
    path = (RESULTS_DIR / task_id / filename).resolve()
    if not path.is_file() or path.parent != (RESULTS_DIR / task_id).resolve():
        raise HTTPException(status_code=404, detail="Not found.")
    return FileResponse(path, media_type="image/png")


@app.get("/api/health", response_model=HealthResponse)
async def health():
    provider = get_provider()
    return HealthResponse(
        status="ok",
        provider_mode=provider.mode,
        provider_ready=provider.ready,
        queue_length=task_queue.queue_length,
        running_task_id=task_queue.running_task_id,
    )


@app.get("/api/stats")
async def stats():
    return db.generation_stats()


@app.get("/api/presets", response_model=PresetListResponse)
async def presets():
    return PresetListResponse(presets=[Preset(**item) for item in PRESET_PROMPTS])


@app.post("/api/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    vocabulary = {
        "向左": "left-facing",
        "向右": "right-facing",
        "正面": "front-facing",
        "女角": "female role",
        "旦角": "female role",
        "男角": "male role",
        "生角": "male role",
        "花脸": "painted-face role",
        "神怪": "mythical character",
        "凤冠": "phoenix crown",
        "王帽": "traditional royal crown",
        "玄黑": "black palette",
        "朱红": "vermilion palette",
        "琥珀黄": "amber palette",
        "翠绿": "emerald palette",
        "靛蓝": "indigo palette",
        "繁密": "intricate carved ornaments",
        "疏朗": "sparse carved ornaments",
    }
    recognized = [word for word in vocabulary if word in request.text]
    phrases = [vocabulary[word] for word in recognized]
    text_en = ""
    if phrases:
        text_en = ", ".join(
            ["Hehuang shadow puppet portrait", *phrases, "pure white background", "centered composition"]
        )
    return TranslateResponse(
        text_en=text_en,
        recognized=recognized,
        unrecognized=[],
        summary_zh="已按识别到的角色、朝向、配色与纹样关键词生成英文描述。" if phrases else "未识别到可用关键词。",
    )


FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"


@app.get("/{full_path:path}", include_in_schema=False)
async def spa_fallback(full_path: str):
    if not FRONTEND_DIST.is_dir():
        raise HTTPException(status_code=404, detail="Frontend not built.")
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="Not found.")
    file = (FRONTEND_DIST / full_path).resolve()
    if full_path and file.is_file() and file.parent.is_relative_to(FRONTEND_DIST.resolve()):
        headers = {"Cache-Control": "public, max-age=31536000, immutable"} if full_path.startswith("assets/") else None
        return FileResponse(file, headers=headers)
    if full_path.startswith("assets/"):
        raise HTTPException(status_code=404, detail="Asset not found.")
    return FileResponse(FRONTEND_DIST / "index.html", headers={"Cache-Control": "no-cache"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
