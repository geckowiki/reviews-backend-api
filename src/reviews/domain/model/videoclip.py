from uuid import UUID
from datetime import datetime

from domain.model.entity import Entity


class Videoclip(Entity[UUID]):
    id: UUID
    name: str
    filepath: str
    uploaded: datetime
    hash_id: str
    author_id: UUID

    def __init__(
        self,
        id: UUID,
        name: str,
        filepath: str,
        uploaded: datetime,
        hash_id: str,
        author_id: UUID,
    ) -> None:
        super().__init__(id=id)
        self.name = name
        self.filepath = filepath
        self.uploaded = uploaded
        self.hash_id = hash_id
        self.author_id = author_id