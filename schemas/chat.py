from pydantic import BaseModel, ConfigDict


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
    date_sent: str


class ChatMessageResponse(ChatMessage):

    sender_id: int
    sender_username: str
