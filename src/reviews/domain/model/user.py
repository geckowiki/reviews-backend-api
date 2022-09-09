from uuid import UUID

from domain.model.entity import Entity


class User(Entity[UUID]):
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

    def __init__(
        self,
        id: UUID,
        email: str,
        hashed_password: str,
        is_active: bool,
        is_superuser: bool,
        is_verified: bool,
    ) -> None:
        super().__init__(id=id)
        self.email = email
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.is_verified = is_verified
