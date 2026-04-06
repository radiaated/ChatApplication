from pydantic import BaseModel


class TokenResponse(BaseModel):

    access: str
