from pydantic import BaseModel

from api.model.position import Position
from api.model.school import School


class SchoolAssignment(BaseModel):
    position: Position
    quantity: int


class PositionAssignment(BaseModel):
    school: School
    quantity: int
