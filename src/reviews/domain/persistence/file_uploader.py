import abc
from typing import BinaryIO


class AbstractFileUploader:
    
    @abc.abstractmethod
    def upload(self, file: BinaryIO, filename: str) -> str:
        ...