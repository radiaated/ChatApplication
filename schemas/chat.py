from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ChatRoomResponse(BaseModel):
    id: int
    name: str
    description: str
    admin_id: int


class ChatRoomCreate(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str


class ChatRoomUpdate(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    description: str | None = None


class ChatMessage(BaseModel):

    message: str
    datetime_sent: datetime


class ChatMessageResponse(ChatMessage):

    model_config = ConfigDict(from_attributes=True)

    id: int
    sender_id: int
