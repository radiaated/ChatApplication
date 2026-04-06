from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Schema for returning an access token."""

    access: str
