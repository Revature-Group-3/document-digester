from typing import Protocol

from document_digester.domain.developer import Developer


class DeveloperRepositoryProtocol(Protocol):
    def get_all(self) -> list[Developer]: ...

    def get_by_id(self, developer_id: int) -> Developer | None: ...

    def get_by_email(self, developer_email: str) -> Developer | None: ...
