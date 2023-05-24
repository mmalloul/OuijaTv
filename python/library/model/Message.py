from dataclasses import dataclass
from typing import Generic, TypeVar, Any
from python.library.model.MessageType import MessageType

T = TypeVar("T", bound=MessageType)


@dataclass
class Message(Generic[T]):
    type: T
    content: str = ""

    @property
    def json(self) -> dict[str, Any]:
        return {
            "type": self.type.value,
            "content": self.content
        }