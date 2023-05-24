from dataclasses import dataclass
from typing import Any
from library.model.MessageType import ClientMessageType, ServerMessageType

# Python generics aren't viable, sadly


@dataclass
class Message:
    type: ClientMessageType | ServerMessageType
    content: str = ""

    @property
    def json(self) -> dict[str, Any]:
        return {
            "type": self.type.value,
            "content": self.content
        }
    

class ClientMessage(Message):

    @staticmethod
    def from_dictionary(dictionary: dict[str, Any]) -> "ClientMessage":
        return ClientMessage(
            ClientMessageType(dictionary["type"]),
            dictionary.get("content", ""),
        )
    

class ServerMessage(Message):

    @staticmethod
    def from_dictionary(dictionary: dict[str, Any]) -> "ServerMessage":
        return ServerMessage(
            ServerMessageType(dictionary["type"]),
            dictionary.get("content", ""),
        )