from uuid import UUID
from dataclasses import dataclass
from typing import BinaryIO

from domain.commands.command import Command


@dataclass
class PostReview(Command):
    image: BinaryIO
    filename: str
    text: str
    videoclip_id: UUID
