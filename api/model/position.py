from pydantic import BaseModel


class Position(BaseModel):
    code: str
    name: str
    corps: str
