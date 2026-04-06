from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ChatRoomCreate(BaseModel):

    name: str
    description: str


class ChatRoomUpdate(BaseModel):

    name: str | None = None
    description: str | None = None


class ChatRoomResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    admin_id: int


class ChatMessage(BaseModel):

    message: str
    datetime_sent: datetime


class ChatMessageRequest(ChatMessage):
    pass


class ChatMessageResponse(ChatMessage):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sender_id: int


class ChatRoomMessageCount(BaseModel):

    id: int
    name: str
    message_count: int
