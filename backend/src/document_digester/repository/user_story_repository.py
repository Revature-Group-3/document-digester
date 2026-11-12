from document_digester.domain.user_story import UserStory
from document_digester.repository.user_story_repository_protocol import (
    UserStoryRepositoryProtocol,
)
from sqlalchemy import select
from sqlalchemy.orm import Session


class UserStoryRepository(UserStoryRepositoryProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[UserStory]:
        return list(self.db.scalars(select(UserStory)).all())

    def get_by_id(self, user_story_id: int) -> UserStory | None:
        return self.db.get(UserStory, user_story_id)
