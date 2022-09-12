from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, UploadFile, Depends, Response, status
from fastapi.responses import FileResponse
from pydantic import BaseModel

from domain.services.message_bus import MessageBus
from domain.commands.create_videoclip import CreateVideoclip
from domain.queries.download_videoclip import DownloadVideoclip
from domain.queries.get_videoclips import GetVideoclips
from adapters.persistence.orm import User
from adapters.persistence.auth import current_active_user
from adapters.http.api_v1.dependencies import dependency_message_bus
from adapters.http.api_v1.response import HttpMethod, build_response


router = APIRouter()


class VideoclipPydanticOut(BaseModel):
    id: UUID
    name: str
    uploaded: datetime
    hash_id: str
    author: UUID


@router.get("/videoclips/")
def get_videoclips(
    response: Response,
    user: User = Depends(current_active_user),
    message_bus: MessageBus = Depends(dependency_message_bus),
):
    query = GetVideoclips()
    result = message_bus.dispatch(query)

    response = build_response(result, HttpMethod.GET)

    return result # TODO: return out model


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


@router.get("/videoclips/{id}/download/")
def download_videoclip(
    id: UUID,
    response: Response,
    user: User = Depends(current_active_user),
    message_bus: MessageBus = Depends(dependency_message_bus),
):
    query = DownloadVideoclip(id)
    result = message_bus.dispatch(query)

    response = build_response(result, HttpMethod.GET)

    return FileResponse(path=result.filepath, media_type="application/octet-stream")
