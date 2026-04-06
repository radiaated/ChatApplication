from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List


class ChatRoomCreate(BaseModel):
    """Schema for creating a chat room."""

    name: str
    description: str


class ChatRoomUpdate(BaseModel):
    """Schema for updating a chat room (partial update allowed)."""

    name: str | None = None
    description: str | None = None


class ChatRoomResponse(BaseModel):
    """Schema for returning chat room details."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    admin_id: int


class ChatMessage(BaseModel):
    """Base schema for chat messages."""

    message: str
    datetime_sent: datetime


class ChatMessageRequest(ChatMessage):
    """Schema for sending a chat message (request)."""

    pass


class ChatMessageResponse(ChatMessage):
    """Schema for returning a chat message (response)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    sender_id: int


class ChatRoomMessageCountResponse(BaseModel):
    """Schema for returning chat room with message count."""

    id: int
    name: str
    message_count: int


class UserMessageCount(BaseModel):
    """Schema for returning a user's message count."""

    user_id: int
    username: str
    message_count: int


class UserRoomCount(BaseModel):
    """Schema for returning a user's room count."""

    user_id: int
    username: str
    room_count: int


class UserActivityResponse(BaseModel):
    """Schema for returning user activity across messages and rooms."""

    messages_count: List[UserMessageCount]
    rooms_count: List[UserRoomCount]
