import uuid
from datetime import datetime

from domain.commands.create_videoclip import CreateVideoclip
from domain.persistence.repository import AbstractRepository
from domain.persistence.file_uploader import AbstractFileUploader
from domain.model.videoclip import Videoclip
from util.hash_id import convert_uuid_to_hashid


def create_videoclip_use_case(
    command: CreateVideoclip,
    file_uploader: AbstractFileUploader,
    videoclip_repository: AbstractRepository[Videoclip],
) -> Videoclip:
    id = uuid.uuid4()
    hash_id = convert_uuid_to_hashid(id)

    destination = file_uploader.upload(command.file, hash_id)

    videoclip = Videoclip(
        id=id,
        name=command.filename,
        filepath=destination,
        uploaded=datetime.now(),
        hash_id=hash_id,
        author_id=command.user.id,
    )
    videoclip_repository.create(videoclip)

    return videoclip
