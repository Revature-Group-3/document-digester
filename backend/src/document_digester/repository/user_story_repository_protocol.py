from typing import Protocol

from document_digester.domain.user_story import UserStory


class UserStoryRepositoryProtocol(Protocol):
    def get_all(self) -> list[UserStory]: ...

    def get_by_id(self, user_story_id: int) -> UserStory | None: ...
