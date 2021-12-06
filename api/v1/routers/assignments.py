from fastapi import APIRouter

from api.utils import db
from api.utils.db import DB_FILE
from api.v1.routers.positions import POSITIONS_TABLE_NAME
from api.v1.routers.schools import SCHOOLS_TABLE_NAME

router = APIRouter()
ASSIGNMENTS_TABLE_NAME = 'assignments'


@router.get("/positions-in-a-school")
def list_positions_assigned_for_a_school(school_code: int):
    return db.query_inner_join(db_file=DB_FILE, table_left=ASSIGNMENTS_TABLE_NAME, table_right=POSITIONS_TABLE_NAME,
                               field_key_left='position', field_key_right='code',
                               field_filters_left={'school': school_code}, field_filters_right={})


@router.get("/schools-with-a-position")
def list_schools_with_specific_position_assigned(position_code: int):
    return db.query_inner_join(db_file=DB_FILE, table_left=ASSIGNMENTS_TABLE_NAME, table_right=SCHOOLS_TABLE_NAME,
                               field_key_left='school', field_key_right='code',
                               field_filters_left={'position': position_code}, field_filters_right={})
