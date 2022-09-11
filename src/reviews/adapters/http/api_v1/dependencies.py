from adapters.persistence.orm import sync_session_maker
from adapters.persistence.repositories import VideoclipRepository
from adapters.persistence.file_uploader import FileUploader
from domain.services.message_bus import MessageBus


def dependency_message_bus():
    with sync_session_maker() as session:
        message_bus = MessageBus(
            file_uploader=FileUploader(),
            videoclip_repository=VideoclipRepository(session),
        )
        return message_bus