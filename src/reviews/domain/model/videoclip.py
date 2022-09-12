from uuid import UUID
from datetime import datetime
from typing import List

from domain.model.entity import Entity
from domain.model.review import Review
from domain.persistence.repository import AbstractRepository


class Videoclip(Entity[UUID]):
    name: str
    filepath: str
    uploaded: datetime
    hash_id: str
    author_id: UUID

    reviews: List[Review]

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

    def add_review(self, review: Review, review_repository: AbstractRepository[Review]):
        review_repository.create(review)
        self.reviews.append(review)

    def __repr__(self) -> str:
        return f"Videoclip({self.id}, {self.hash_id})"
