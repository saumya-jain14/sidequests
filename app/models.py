from sqlalchemy import Column, String, Text, Enum, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid

from .database import Base


def new_id():
    return str(uuid.uuid4())


# Many-to-many join table between quests and tags
quest_tags = Table(
    "quest_tags",
    Base.metadata,
    Column("quest_id", String, ForeignKey("quests.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id",   String, ForeignKey("tags.id",   ondelete="CASCADE"), primary_key=True),
)


class StatusEnum(str, enum.Enum):
    todo    = "todo"
    done    = "done"
    skipped = "skipped"


class Quest(Base):
    __tablename__ = "quests"

    id          = Column(String, primary_key=True, default=new_id)
    title       = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status      = Column(Enum(StatusEnum), default=StatusEnum.todo, nullable=False)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), onupdate=func.now())

    tags = relationship("Tag", secondary=quest_tags, back_populates="quests")


class Tag(Base):
    __tablename__ = "tags"

    id    = Column(String, primary_key=True, default=new_id)
    name  = Column(String(50), unique=True, nullable=False)
    color = Column(String(7), nullable=False, default="#888888")  # hex color

    quests = relationship("Quest", secondary=quest_tags, back_populates="tags")
