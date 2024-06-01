from pydantic import BaseModel


class SendTextMessage(BaseModel):
    message: str
    temperature: float = 0.87
