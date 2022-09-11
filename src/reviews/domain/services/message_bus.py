from typing import Union, List

from domain.commands.command import Command
from domain.queries.query import Query
from domain.commands.create_videoclip import CreateVideoclip
from domain.persistence.repository import AbstractRepository
from domain.persistence.file_uploader import AbstractFileUploader
from domain.model.videoclip import Videoclip
from domain.services.use_cases import create_videoclip_use_case


Message = Union[Command, Query]
Result = Union[Videoclip, None]


class MessageBus:

    COMMAND_HANDLERS = {CreateVideoclip: create_videoclip_use_case}
    QUERY_HANDLERS = {}

    videoclip_repository: AbstractRepository[Videoclip]
    file_uploader: AbstractFileUploader

    def __init__(self, file_uploader: AbstractFileUploader, videoclip_repository: AbstractRepository[Videoclip]):
        self.file_uploader = file_uploader
        self.videoclip_repository = videoclip_repository

    def dispatch(self, message: Message) -> Result:
        if isinstance(message, Command):
            handler = self.COMMAND_HANDLERS[type(message)]
            return handler(message, self.file_uploader, self.videoclip_repository)
