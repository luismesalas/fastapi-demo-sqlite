from pydantic import BaseModel


class GenericMessage(BaseModel):
    message: str


class GenericExceptionMessage(BaseModel):
    status_code: int
    detail: str
