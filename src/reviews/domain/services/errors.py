from uuid import UUID
from dataclasses import dataclass


@dataclass
class VideoclipNotFound:
    videoclip_id: UUID