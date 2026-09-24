"""Pydantic models for the portfolio API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


def normalize_candidate_score(value: Any) -> dict[str, float]:
    """Normalize provider score payloads to the public product contract.

    The private generation service may use its own field names. The public
    repository exposes only three product-level scores and never forwards the
    provider's internal names to the browser.
    """
    if not isinstance(value, dict):
        raise ValueError("A candidate score must be an object.")

    public_keys = ("outline_similarity", "detail_similarity", "overall_score")
    if all(key in value for key in public_keys):
        numbers = [value[key] for key in public_keys]
    else:
        numbers = [item for item in value.values() if isinstance(item, (int, float)) and not isinstance(item, bool)]

    if len(numbers) < 3:
        raise ValueError("A candidate score must contain three numeric values.")
    return {key: round(float(number), 4) for key, number in zip(public_keys, numbers[:3])}


class GenerateResponse(BaseModel):
    task_id: str
    position: int


class CandidateScore(BaseModel):
    outline_similarity: float
    detail_similarity: float
    overall_score: float


class TaskResult(BaseModel):
    candidate_urls: list[str]
    candidate_scores: list[CandidateScore]
    selected_index: int
    selected_url: str
    final_url: str
    condition_simple_url: str
    condition_complex_url: str
    elapsed_seconds: float
    simple_mode: str = "auto"


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    position: int | None
    created_at: float
    error: str | None = None
    result: TaskResult | None = None


class HistoryItem(BaseModel):
    task_id: str
    created_at: float
    status: str
    prompt_preview: str
    thumbnail_url: str | None
    elapsed_seconds: float | None


class HistoryListResponse(BaseModel):
    total: int
    items: list[HistoryItem]


class HistoryDetailResponse(BaseModel):
    task_id: str
    created_at: float
    status: str
    prompt: str
    negative_prompt: str | None
    params: dict[str, Any]
    error: str | None = None
    result: TaskResult | None = None


class HealthResponse(BaseModel):
    status: str
    provider_mode: str
    provider_ready: bool
    queue_length: int
    running_task_id: str | None


class Preset(BaseModel):
    name: str
    prompt: str


class PresetListResponse(BaseModel):
    presets: list[Preset]


class TranslateRequest(BaseModel):
    text: str


class TranslateResponse(BaseModel):
    text_en: str
    recognized: list[str]
    unrecognized: list[str]
    summary_zh: str
