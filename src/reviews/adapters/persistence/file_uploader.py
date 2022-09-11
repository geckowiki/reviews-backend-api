from pathlib import Path
import shutil
from typing import BinaryIO

from domain.persistence.file_uploader import AbstractFileUploader
from app.settings import settings


class FileUploader(AbstractFileUploader):
    def upload(self, file: BinaryIO, filename: str) -> str:
        media_root = settings.MEDIA_ROOT
        path = Path(media_root)

        if path.exists() is False:
            path.mkdir()

        destination = path / filename

        try:
            with open(destination, "wb") as f:
                shutil.copyfileobj(file, f)
        finally:
            file.close()

        return str(destination)
