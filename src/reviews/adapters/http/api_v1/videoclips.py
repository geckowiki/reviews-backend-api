from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, UploadFile, Depends, Response, status
from pydantic import BaseModel

from domain.services.message_bus import MessageBus
from domain.commands.create_videoclip import CreateVideoclip
from adapters.http.api_v1.dependencies import dependency_message_bus
from adapters.persistence.orm import User
from adapters.persistence.auth import current_active_user


router = APIRouter()


class VideoclipPydanticOut(BaseModel):
    id: UUID
    name: str
    uploaded: datetime
    hash_id: str
    author: UUID


@router.post("/videoclips/")
def upload_videoclip(
    upload_file: UploadFile,
    response: Response,
    user: User = Depends(current_active_user),
    message_bus: MessageBus = Depends(dependency_message_bus),
):
    command = CreateVideoclip(user.to_domain(), upload_file.file, upload_file.filename)
    result = message_bus.dispatch(command)

    response.status_code = status.HTTP_201_CREATED

    return VideoclipPydanticOut(
        id=result.id,
        name=result.name,
        uploaded=result.uploaded,
        hash_id=result.hash_id,
        author=result.author_id,
    )
