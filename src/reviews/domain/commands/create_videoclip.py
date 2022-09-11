from dataclasses import dataclass
from typing import BinaryIO

from domain.commands.command import Command


@dataclass
class CreateVideoclip(Command):
    file: BinaryIO
    filename: str
