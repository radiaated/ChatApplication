from pydantic import BaseModel


class ChatMessage(BaseModel):

    message: str
    date_sent: str


class ChatMessageResponse(ChatMessage):

    sender_id: int
    sender_username: str
