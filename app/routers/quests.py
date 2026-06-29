import random
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Quest, Tag, StatusEnum
from ..schemas import QuestCreate, QuestUpdate, QuestOut

router = APIRouter()


def get_quest_or_404(quest_id: str, db: Session) -> Quest:
    q = db.query(Quest).filter(Quest.id == quest_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Quest not found")
    return q


@router.get("/", response_model=list[QuestOut])
def list_quests(
    q:      Optional[str]        = Query(None, description="Search in title and description"),
    tags:   Optional[str]        = Query(None, description="Comma-separated tag IDs to filter by (AND logic)"),
    status: Optional[StatusEnum] = Query(None),
    db:     Session              = Depends(get_db),
):
    """Return all quests, with optional search, tag filter, and status filter."""
    query = db.query(Quest)

    if status:
        query = query.filter(Quest.status == status)

    if q:
        like = f"%{q}%"
        query = query.filter(
            Quest.title.ilike(like) | Quest.description.ilike(like)
        )

    if tags:
        tag_ids = [t.strip() for t in tags.split(",") if t.strip()]
        for tag_id in tag_ids:
            query = query.filter(Quest.tags.any(Tag.id == tag_id))

    return query.order_by(Quest.created_at.desc()).all()


@router.get("/random", response_model=QuestOut)
def random_quest(
    tags:   Optional[str] = Query(None, description="Comma-separated tag IDs"),
    db:     Session        = Depends(get_db),
):
    """Return a random todo quest, optionally filtered by tags."""
    query = db.query(Quest).filter(Quest.status == StatusEnum.todo)

    if tags:
        tag_ids = [t.strip() for t in tags.split(",") if t.strip()]
        for tag_id in tag_ids:
            query = query.filter(Quest.tags.any(Tag.id == tag_id))

    pool = query.all()
    if not pool:
        raise HTTPException(status_code=404, detail="No quests available with those filters")

    return random.choice(pool)


@router.get("/{quest_id}", response_model=QuestOut)
def get_quest(quest_id: str, db: Session = Depends(get_db)):
    return get_quest_or_404(quest_id, db)


@router.post("/", response_model=QuestOut, status_code=201)
def create_quest(body: QuestCreate, db: Session = Depends(get_db)):
    quest = Quest(title=body.title, description=body.description)

    if body.tag_ids:
        quest.tags = db.query(Tag).filter(Tag.id.in_(body.tag_ids)).all()

    db.add(quest)
    db.commit()
    db.refresh(quest)
    return quest


@router.patch("/{quest_id}", response_model=QuestOut)
def update_quest(quest_id: str, body: QuestUpdate, db: Session = Depends(get_db)):
    quest = get_quest_or_404(quest_id, db)

    if body.title is not None:
        quest.title = body.title
    if body.description is not None:
        quest.description = body.description
    if body.status is not None:
        quest.status = body.status
    if body.tag_ids is not None:
        quest.tags = db.query(Tag).filter(Tag.id.in_(body.tag_ids)).all()

    db.commit()
    db.refresh(quest)
    return quest


@router.delete("/{quest_id}", status_code=204)
def delete_quest(quest_id: str, db: Session = Depends(get_db)):
    quest = get_quest_or_404(quest_id, db)
    db.delete(quest)
    db.commit()
