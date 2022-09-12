from dataclasses import dataclass

from domain.model.user import User


@dataclass
class Command:
    user: User
