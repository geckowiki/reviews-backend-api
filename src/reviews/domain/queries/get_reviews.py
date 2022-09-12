from uuid import UUID
from dataclasses import dataclass

from domain.queries.query import Query


@dataclass
class GetReviews(Query):
    videoclip_id: UUID
