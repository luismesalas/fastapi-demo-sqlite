from pydantic import BaseModel


class School(BaseModel):
    code: int
    name: str
    province: str
    locality: str
