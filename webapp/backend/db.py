"""SQLite persistence for generation jobs."""

from __future__ import annotations

import json
import sqlite3
import time
from typing import Any

from .config import DB_PATH, ensure_data_dirs

_SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL,
    status TEXT NOT NULL,
    prompt TEXT NOT NULL,
    negative_prompt TEXT,
    params_json TEXT,
    candidate_count INTEGER,
    candidate_scores_json TEXT,
    selected_index INTEGER,
    elapsed_seconds REAL,
    error TEXT,
    upload_filename TEXT
);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at DESC);
"""


def _connect() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    ensure_data_dirs()
    with _connect() as connection:
        connection.executescript(_SCHEMA)


def insert_task(
    task_id: str,
    prompt: str,
    negative_prompt: str | None,
    params: dict[str, Any],
    upload_filename: str | None,
) -> None:
    now = time.time()
    with _connect() as connection:
        connection.execute(
            "INSERT INTO tasks (id, created_at, updated_at, status, prompt, "
            "negative_prompt, params_json, upload_filename) "
            "VALUES (?, ?, ?, 'queued', ?, ?, ?, ?)",
            (
                task_id,
                now,
                now,
                prompt,
                negative_prompt,
                json.dumps(params, ensure_ascii=False),
                upload_filename,
            ),
        )


def update_status(task_id: str, status: str, error: str | None = None) -> None:
    with _connect() as connection:
        connection.execute(
            "UPDATE tasks SET status = ?, error = ?, updated_at = ? WHERE id = ?",
            (status, error, time.time(), task_id),
        )


def complete_task(
    task_id: str,
    candidate_scores: list[dict[str, float]],
    selected_index: int,
    elapsed_seconds: float,
) -> None:
    with _connect() as connection:
        connection.execute(
            "UPDATE tasks SET status = 'done', candidate_count = ?, candidate_scores_json = ?, "
            "selected_index = ?, elapsed_seconds = ?, updated_at = ? WHERE id = ?",
            (
                len(candidate_scores),
                json.dumps(candidate_scores),
                selected_index,
                elapsed_seconds,
                time.time(),
                task_id,
            ),
        )


def get_task(task_id: str) -> dict[str, Any] | None:
    with _connect() as connection:
        row = connection.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return dict(row) if row else None


def list_tasks(limit: int = 20, offset: int = 0) -> tuple[int, list[dict[str, Any]]]:
    limit = max(1, min(limit, 100))
    offset = max(0, offset)
    with _connect() as connection:
        total = connection.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        rows = connection.execute(
            "SELECT * FROM tasks ORDER BY created_at DESC LIMIT ? OFFSET ?",
            (limit, offset),
        ).fetchall()
    return total, [dict(row) for row in rows]


def generation_stats() -> dict[str, int]:
    with _connect() as connection:
        row = connection.execute(
            "SELECT COUNT(*) AS completed, COALESCE(SUM(candidate_count), 0) AS candidates "
            "FROM tasks WHERE status = 'done'"
        ).fetchone()
    return {
        "completed_generations": int(row["completed"]),
        "total_candidates": int(row["candidates"]),
    }
