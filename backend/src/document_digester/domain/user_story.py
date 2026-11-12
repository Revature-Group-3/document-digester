from document_digester.domain.base import Base
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column


class UserStory(Base):
    __tablename__ = "user_story"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    assignee_id: Mapped[int | None] = mapped_column(
        ForeignKey("developer.id"),
        nullable=True
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
