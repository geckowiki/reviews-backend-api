from uuid import UUID
from datetime import datetime

from domain.model.entity import Entity


class Review(Entity[UUID]):
    imagepath: str
    text: str
    published: datetime
    hash_id: str
    videoclip_id: UUID
    author_id: UUID

    def __init__(
        self,
        id: UUID,
        imagepath: str,
        text: str,
        published: datetime,
        hash_id: str,
        videoclip_id: UUID,
        author_id: UUID,
    ) -> None:
        super().__init__(id=id)
        self.imagepath = imagepath
        self.text = text
        self.published = published
        self.hash_id = hash_id
        self.videoclip_id = videoclip_id
        self.author_id = author_id

    def __repr__(self) -> str:
        return f"Review({self.id}, {self.hash_id})"
