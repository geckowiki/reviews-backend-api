import uuid
from datetime import datetime

from fastapi import APIRouter, UploadFile, Depends, Form, Response
from pydantic import BaseModel

from domain.services.message_bus import MessageBus
from domain.commands.post_review import PostReview
from domain.queries.get_reviews import GetReviews
from adapters.http.api_v1.dependencies import dependency_message_bus
from adapters.persistence.orm import User
from adapters.persistence.auth import current_active_user
from adapters.http.api_v1.response import HttpMethod, build_response


router = APIRouter()


class ReviewPydanticOut(BaseModel):
    id: uuid.UUID
    text: str
    published: datetime
    hash_id: str
    videoclip_id: uuid.UUID
    author_id: uuid.UUID


@router.get("/{videoclip_id}/reviews/")
def get_reviews(
    videoclip_id: uuid.UUID,
    response: Response,
    skip: int = 0,
    limit: int = 10,
    user: User = Depends(current_active_user),
    message_bus: MessageBus = Depends(dependency_message_bus),
):
    query = GetReviews(videoclip_id)
    result = message_bus.dispatch(query)

    response = build_response(result, HttpMethod.GET)

    return result[skip : skip + limit] # TODO: out model


@router.post("/reviews/")
def create_review(
    upload_file: UploadFile,
    response: Response,
    text: str = Form(),
    videoclip_id: str = Form(),
    user: User = Depends(current_active_user),
    message_bus: MessageBus = Depends(dependency_message_bus),
):
    command = PostReview(
        user.to_domain(), upload_file.file, upload_file.filename, text, uuid.UUID(videoclip_id).hex
    )
    result = message_bus.dispatch(command)

    response = build_response(result, HttpMethod.GET)

    return result # TODO: out model
