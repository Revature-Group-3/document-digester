from document_digester.domain.developer import Developer
from document_digester.repository.developer_repository_protocol import (
    DeveloperRepositoryProtocol,
)
from sqlalchemy import select
from sqlalchemy.orm import Session


class DeveloperRepository(DeveloperRepositoryProtocol):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[Developer]:
        return list(self.db.scalars(select(Developer)).all())

    def get_by_id(self, developer_id: int) -> Developer | None:
        return self.db.get(Developer, developer_id)

    def get_by_email(self, developer_email: str) -> Developer | None:
        return self.db.scalar(select(Developer).where(Developer.email == developer_email))
