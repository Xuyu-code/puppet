"""Generation provider boundary.

The portfolio repository deliberately treats image generation as an external
service. The mock provider keeps the product workflow runnable without model
assets; the remote provider forwards requests to a protected deployment.
"""

from __future__ import annotations

import base64
import io
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import httpx
from PIL import Image, ImageEnhance, ImageOps

from .config import (
    PROVIDER_API_KEY,
    PROVIDER_MODE,
    PROVIDER_TIMEOUT_SECONDS,
    PROVIDER_URL,
)
from .schemas import normalize_candidate_score


@dataclass
class ProviderOutput:
    candidates: list[Image.Image]
    candidate_scores: list[dict[str, float]]
    selected_index: int
    simple_condition: Image.Image
    complex_condition: Image.Image
    final_image: Image.Image
    simple_mode: str = "auto"


class GenerationProvider(Protocol):
    mode: str

    @property
    def ready(self) -> bool: ...

    def generate(
        self,
        lineart_path: Path,
        simple_lineart_path: Path | None,
        prompt: str,
        negative_prompt: str | None,
        candidate_count: int,
        steps: int,
        guidance_scale: float,
        conditioning_scale: float,
        simple_weight: float,
        complex_weight: float,
        seed: int,
        postprocess: bool,
    ) -> ProviderOutput: ...


class MockGenerationProvider:
    """Produce deterministic placeholders for UI and API development."""

    mode = "mock"

    @property
    def ready(self) -> bool:
        return True

    def generate(
        self,
        lineart_path: Path,
        simple_lineart_path: Path | None,
        prompt: str,
        negative_prompt: str | None,
        candidate_count: int,
        steps: int,
        guidance_scale: float,
        conditioning_scale: float,
        simple_weight: float,
        complex_weight: float,
        seed: int,
        postprocess: bool,
    ) -> ProviderOutput:
        del prompt, negative_prompt, steps, guidance_scale, conditioning_scale, seed, postprocess
        with Image.open(lineart_path) as source:
            source_preview = ImageOps.fit(source.convert("RGB"), (768, 768))
            gray = ImageOps.autocontrast(source_preview.convert("L"))
        if simple_lineart_path is not None:
            with Image.open(simple_lineart_path) as source:
                simple_condition = ImageOps.autocontrast(ImageOps.fit(source.convert("L"), (768, 768))).convert("RGB")
            simple_mode = "expert"
        else:
            simple_condition = source_preview.copy()
            simple_mode = "auto"
        complex_condition = source_preview.copy()

        ink = ImageEnhance.Contrast(ImageOps.invert(gray)).enhance(1.6)
        palettes = [
            ((249, 244, 229), (54, 38, 28)),
            ((242, 232, 206), (143, 47, 35)),
            ((235, 239, 228), (37, 73, 61)),
            ((235, 229, 220), (41, 63, 88)),
            ((245, 235, 211), (105, 67, 38)),
            ((231, 237, 240), (65, 45, 76)),
        ]
        candidates: list[Image.Image] = []
        for index in range(candidate_count):
            background, foreground = palettes[index % len(palettes)]
            canvas = Image.new("RGB", gray.size, background)
            strokes = Image.new("RGB", gray.size, foreground)
            canvas.paste(strokes, mask=ink)
            canvas = ImageOps.expand(canvas, border=18, fill=(181, 143, 70))
            canvas = ImageOps.expand(canvas, border=8, fill=(250, 247, 238))
            candidates.append(canvas)
        # Fixed sample values exercise the product UI without reproducing the
        # private service's image metric implementation.
        demo_scores = [
            (0.86, 0.83),
            (0.81, 0.79),
            (0.78, 0.76),
        ]
        candidate_scores = [
            {
                "outline_similarity": demo_scores[index % len(demo_scores)][0],
                "detail_similarity": demo_scores[index % len(demo_scores)][1],
                "overall_score": round(
                    simple_weight * demo_scores[index % len(demo_scores)][0]
                    + complex_weight * demo_scores[index % len(demo_scores)][1],
                    4,
                ),
            }
            for index in range(candidate_count)
        ]
        selected_index = max(range(candidate_count), key=lambda index: candidate_scores[index]["overall_score"])
        return ProviderOutput(
            candidates=candidates,
            candidate_scores=candidate_scores,
            selected_index=selected_index,
            simple_condition=simple_condition,
            complex_condition=complex_condition,
            final_image=candidates[selected_index],
            simple_mode=simple_mode,
        )


class RemoteGenerationProvider:
    mode = "remote"

    @property
    def ready(self) -> bool:
        return bool(PROVIDER_URL)

    @staticmethod
    def _decode_image(value: str) -> Image.Image:
        payload = value.split(",", 1)[-1]
        raw = base64.b64decode(payload, validate=True)
        with Image.open(io.BytesIO(raw)) as image:
            return image.convert("RGB").copy()

    def generate(
        self,
        lineart_path: Path,
        simple_lineart_path: Path | None,
        prompt: str,
        negative_prompt: str | None,
        candidate_count: int,
        steps: int,
        guidance_scale: float,
        conditioning_scale: float,
        simple_weight: float,
        complex_weight: float,
        seed: int,
        postprocess: bool,
    ) -> ProviderOutput:
        if not self.ready:
            raise RuntimeError("PUPPET_GENERATION_API_URL is not configured.")
        headers = {"Authorization": f"Bearer {PROVIDER_API_KEY}"} if PROVIDER_API_KEY else {}
        data = {
            "prompt": prompt,
            "negative_prompt": negative_prompt or "",
            "candidate_count": str(candidate_count),
            "steps": str(steps),
            "guidance_scale": str(guidance_scale),
            "conditioning_scale": str(conditioning_scale),
            "simple_weight": str(simple_weight),
            "complex_weight": str(complex_weight),
            "seed": str(seed),
            "postprocess": str(postprocess).lower(),
        }
        with lineart_path.open("rb") as stream:
            files = {"lineart": (lineart_path.name, stream, "application/octet-stream")}
            simple_stream = simple_lineart_path.open("rb") if simple_lineart_path is not None else None
            if simple_stream is not None:
                files["simple_lineart"] = (simple_lineart_path.name, simple_stream, "application/octet-stream")
            response = httpx.post(
                PROVIDER_URL,
                headers=headers,
                data=data,
                files=files,
                timeout=PROVIDER_TIMEOUT_SECONDS,
            )
            if simple_stream is not None:
                simple_stream.close()
        response.raise_for_status()
        body = response.json()
        encoded = body.get("candidates") or []
        if not encoded:
            raise RuntimeError("The generation service returned no candidates.")
        candidates = [self._decode_image(item) for item in encoded]
        selected_index = int(body.get("selected_index", 0))
        if not 0 <= selected_index < len(candidates):
            selected_index = 0
        raw_scores = body.get("candidate_scores") or []
        if len(raw_scores) != len(candidates):
            raise RuntimeError("The generation service returned incomplete candidate scores.")
        candidate_scores = [normalize_candidate_score(item) for item in raw_scores]
        with Image.open(lineart_path) as source:
            complex_condition = source.convert("RGB").copy()
        if body.get("condition_complex"):
            complex_condition = self._decode_image(body["condition_complex"])
        if body.get("condition_simple"):
            simple_condition = self._decode_image(body["condition_simple"])
        elif simple_lineart_path is not None:
            with Image.open(simple_lineart_path) as source:
                simple_condition = source.convert("RGB").copy()
        else:
            simple_condition = complex_condition.copy()
        final_image = self._decode_image(body["final_image"]) if body.get("final_image") else candidates[selected_index]
        return ProviderOutput(
            candidates=candidates,
            candidate_scores=candidate_scores,
            selected_index=selected_index,
            simple_condition=simple_condition,
            complex_condition=complex_condition,
            final_image=final_image,
            simple_mode="expert" if simple_lineart_path is not None else "auto",
        )


_provider: GenerationProvider | None = None


def get_provider() -> GenerationProvider:
    global _provider
    if _provider is None:
        _provider = RemoteGenerationProvider() if PROVIDER_MODE == "remote" else MockGenerationProvider()
    return _provider
