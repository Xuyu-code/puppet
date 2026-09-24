"""In-memory serial task queue for generation requests."""

from __future__ import annotations

import queue
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import db
from .config import RESULTS_DIR
from .provider import get_provider


@dataclass
class Task:
    task_id: str
    lineart_path: Path
    prompt: str
    negative_prompt: str | None
    params: dict[str, Any]
    simple_lineart_path: Path | None = None
    status: str = "queued"
    created_at: float = field(default_factory=time.time)
    error: str | None = None
    result: dict[str, Any] | None = None


class TaskQueue:
    def __init__(self) -> None:
        self._queue: queue.Queue[Task] = queue.Queue()
        self._tasks: dict[str, Task] = {}
        self._pending_ids: list[str] = []
        self._lock = threading.Lock()
        self._running_id: str | None = None
        self._worker: threading.Thread | None = None

    def start(self) -> None:
        if self._worker is not None:
            return
        self._worker = threading.Thread(target=self._work_loop, name="generate-worker", daemon=True)
        self._worker.start()

    def enqueue(
        self,
        task_id: str,
        lineart_path: Path,
        prompt: str,
        negative_prompt: str | None,
        params: dict[str, Any],
        simple_lineart_path: Path | None = None,
    ) -> tuple[Task, int]:
        task = Task(task_id, lineart_path, prompt, negative_prompt, params, simple_lineart_path)
        with self._lock:
            self._tasks[task_id] = task
            self._pending_ids.append(task_id)
            position = len(self._pending_ids)
        db.insert_task(task_id, prompt, negative_prompt, params, lineart_path.name)
        self._queue.put(task)
        return task, position

    def get(self, task_id: str) -> Task | None:
        with self._lock:
            return self._tasks.get(task_id)

    def position_of(self, task_id: str) -> int | None:
        with self._lock:
            return self._pending_ids.index(task_id) + 1 if task_id in self._pending_ids else None

    @property
    def queue_length(self) -> int:
        with self._lock:
            return len(self._pending_ids)

    @property
    def running_task_id(self) -> str | None:
        with self._lock:
            return self._running_id

    def _work_loop(self) -> None:
        provider = get_provider()
        while True:
            task = self._queue.get()
            with self._lock:
                if task.task_id in self._pending_ids:
                    self._pending_ids.remove(task.task_id)
                self._running_id = task.task_id
                task.status = "running"
            db.update_status(task.task_id, "running")
            try:
                started = time.perf_counter()
                output = provider.generate(
                    lineart_path=task.lineart_path,
                    simple_lineart_path=task.simple_lineart_path,
                    prompt=task.prompt,
                    negative_prompt=task.negative_prompt,
                    candidate_count=task.params["candidate_count"],
                    steps=task.params["steps"],
                    guidance_scale=task.params["guidance_scale"],
                    conditioning_scale=task.params["conditioning_scale"],
                    simple_weight=task.params["simple_weight"],
                    complex_weight=task.params["complex_weight"],
                    seed=task.params["seed"],
                    postprocess=task.params["postprocess"],
                )
                elapsed = time.perf_counter() - started
                result = self._save_outputs(task, output, elapsed)
                db.complete_task(task.task_id, output.candidate_scores, output.selected_index, elapsed)
                with self._lock:
                    task.status = "done"
                    task.result = result
            except Exception as exc:  # noqa: BLE001
                db.update_status(task.task_id, "failed", error=str(exc))
                with self._lock:
                    task.status = "failed"
                    task.error = str(exc)
            finally:
                with self._lock:
                    self._running_id = None
                self._queue.task_done()

    @staticmethod
    def _save_outputs(
        task: Task,
        output,
        elapsed: float,
    ) -> dict[str, Any]:
        task_dir = RESULTS_DIR / task.task_id
        task_dir.mkdir(parents=True, exist_ok=True)

        def url(filename: str) -> str:
            return f"/api/images/{task.task_id}/{filename}"

        output.simple_condition.save(task_dir / "condition_simple.png")
        output.complex_condition.save(task_dir / "condition_complex.png")

        candidate_urls = []
        for index, image in enumerate(output.candidates):
            filename = f"candidate_{index + 1}.png"
            image.save(task_dir / filename)
            candidate_urls.append(url(filename))

        selected = output.candidates[output.selected_index]
        selected.save(task_dir / "selected.png")
        output.final_image.save(task_dir / "final.png")
        return {
            "candidate_urls": candidate_urls,
            "candidate_scores": output.candidate_scores,
            "selected_index": output.selected_index,
            "selected_url": url("selected.png"),
            "final_url": url("final.png"),
            "condition_simple_url": url("condition_simple.png"),
            "condition_complex_url": url("condition_complex.png"),
            "elapsed_seconds": round(elapsed, 3),
            "simple_mode": output.simple_mode,
        }


task_queue = TaskQueue()
