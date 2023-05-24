from dataclasses import dataclass
from typing import Generic, TypeVar
from python.library.model.MessageType import MessageType

T = TypeVar("T", bound=MessageType)


@dataclass
class Message(Generic[T]):
    type: T
    content: str
