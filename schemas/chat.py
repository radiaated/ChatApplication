from pydantic import BaseModel, ConfigDict
from datetime import datetime

from typing import List


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


class ChatRoomMessageCountResponse(BaseModel):

    id: int
    name: str
    message_count: int


class UserMessageCount(BaseModel):

    user_id: int
    username: str
    message_count: int


class UserRoomCount(BaseModel):

    user_id: int
    username: str
    room_count: int


class UserActivityResponse(BaseModel):

    messages_count: List[UserMessageCount]
    rooms_count: List[UserRoomCount]
