"""Pydantic models for JSON entry points (news + video scripts)."""

from __future__ import annotations

from pydantic import BaseModel, Field, ValidationError, field_validator


class SchemaError(ValueError):
    """Raised when inbound JSON fails schema validation."""


class NewsItem(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    source: str = Field(default="", max_length=4000)
    reasoning: str | None = None
    url: str | None = Field(default=None, max_length=2000)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("title must not be blank")
        return cleaned

    @field_validator("url")
    @classmethod
    def url_must_be_http_when_set(cls, value: str | None) -> str | None:
        if value is None or value == "":
            return None
        if not (value.startswith("http://") or value.startswith("https://")):
            raise ValueError("url must start with http:// or https://")
        return value


class Scene(BaseModel):
    narration: str = Field(default="", max_length=8000)
    image_prompt: str = Field(default="", max_length=4000)


class ScriptEntry(BaseModel):
    project_name: str = Field(min_length=1, max_length=200)
    scenes: list[Scene] = Field(default_factory=list)

    @field_validator("project_name")
    @classmethod
    def project_name_strip(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("project_name must not be blank")
        return cleaned


def parse_news_items(raw: object) -> list[NewsItem]:
    if not isinstance(raw, list):
        raise SchemaError("news payload must be a JSON list")
    try:
        return [NewsItem.model_validate(item) for item in raw]
    except ValidationError as exc:
        raise SchemaError(str(exc)) from exc


def parse_script_entries(raw: object) -> list[ScriptEntry]:
    if not isinstance(raw, list):
        raise SchemaError("scripts payload must be a JSON list")
    try:
        return [ScriptEntry.model_validate(item) for item in raw]
    except ValidationError as exc:
        raise SchemaError(str(exc)) from exc


__all__ = [
    "NewsItem",
    "Scene",
    "ScriptEntry",
    "SchemaError",
    "ValidationError",
    "parse_news_items",
    "parse_script_entries",
]
