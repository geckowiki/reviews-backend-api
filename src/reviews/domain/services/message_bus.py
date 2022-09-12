from typing import Union

from domain.commands.command import Command
from domain.queries.query import Query
from domain.commands.create_videoclip import CreateVideoclip
from domain.queries.get_reviews import GetReviews
from domain.queries.download_videoclip import DownloadVideoclip
from domain.queries.get_videoclips import GetVideoclips
from domain.commands.post_review import PostReview
from domain.persistence.repository import AbstractRepository
from domain.persistence.file_uploader import AbstractFileUploader
from domain.model.videoclip import Videoclip
from domain.model.review import Review
from domain.services.use_cases import (
    create_videoclip_use_case,
    download_videoclip_use_case,
    post_review_use_case,
    get_reviews_use_case,
    get_videoclips_use_case,
    Result,
)


Message = Union[Command, Query]


class MessageBus:

    COMMAND_HANDLERS = {
        CreateVideoclip: create_videoclip_use_case,
        PostReview: post_review_use_case,
    }
    QUERY_HANDLERS = {
        GetReviews: get_reviews_use_case,
        DownloadVideoclip: download_videoclip_use_case,
        GetVideoclips: get_videoclips_use_case,
    }

    videoclip_repository: AbstractRepository[Videoclip]
    review_repositoty: AbstractRepository[Review]
    file_uploader: AbstractFileUploader

    def __init__(
        self,
        file_uploader: AbstractFileUploader,
        videoclip_repository: AbstractRepository[Videoclip],
        review_repository: AbstractRepository[Review],
    ):
        self.file_uploader = file_uploader
        self.videoclip_repository = videoclip_repository
        self.review_repositoty = review_repository

    def dispatch(self, message: Message) -> Result:
        if isinstance(message, Command):
            handler = self.COMMAND_HANDLERS[type(message)]
        elif isinstance(message, Query):
            handler = self.QUERY_HANDLERS[type(message)]

        return handler(
            message,
            file_uploader=self.file_uploader,
            videoclip_repository=self.videoclip_repository,
            review_repository=self.review_repositoty,
        )
