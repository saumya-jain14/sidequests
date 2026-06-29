from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .models import StatusEnum


# ── Tag schemas ────────────────────────────────────────────────────────────

class TagBase(BaseModel):
    name:  str = Field(..., min_length=1, max_length=50)
    color: str = Field("#888888", pattern=r"^#[0-9a-fA-F]{6}$")


class TagCreate(TagBase):
    pass


class TagOut(TagBase):
    id: str

    class Config:
        from_attributes = True


# ── Quest schemas ──────────────────────────────────────────────────────────

class QuestBase(BaseModel):
    title:       str  = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


class QuestCreate(QuestBase):
    tag_ids: list[str] = []


class QuestUpdate(BaseModel):
    title:       Optional[str]        = Field(None, min_length=1, max_length=200)
    description: Optional[str]        = None
    status:      Optional[StatusEnum] = None
    tag_ids:     Optional[list[str]]  = None


class QuestOut(QuestBase):
    id:         str
    status:     StatusEnum
    tags:       list[TagOut] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
