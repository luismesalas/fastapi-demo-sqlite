from typing import Optional

from fastapi import APIRouter, HTTPException, status

from api.utils import db
from api.utils.db import DB_FILE

router = APIRouter()
POSITIONS_TABLE_NAME = 'positions'


@router.get("")
def list_positions(name: Optional[str] = None, corps: Optional[str] = None):
    fields = {}
    if name:
        fields['name'] = name
    if corps:
        fields['corps'] = corps

    return db.query_db(db_file=DB_FILE, table=POSITIONS_TABLE_NAME, fields=fields)


@router.post("")
def insert_position(code: int, name: str, corps: str):
    fields = {}
    if code:
        fields['code'] = code
    if name:
        fields['name'] = name
    if corps:
        fields['corps'] = corps

    if not db.insert_db(db_file=DB_FILE, table=POSITIONS_TABLE_NAME, fields=fields):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Position with code {code} already exists in DB.")

    return f"Position with code {code} created"


@router.put("")
def update_position(code: int, name: Optional[str] = None, corps: Optional[str] = None):
    if not name and not corps:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No fields to update in position with code {code}, "
                                   f"please provide a new name or corps at least.")
    fields = {}
    if name:
        fields['name'] = name
    if corps:
        fields['corps'] = corps

    if not db.update_db(db_file=DB_FILE, table=POSITIONS_TABLE_NAME, field_id_name='code', field_id_value=code,
                        fields_to_update=fields):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Can't update position with code {code}")

    return f"Position with code {code} updated"


@router.delete("")
def delete_position(code: int):
    if not db.delete_db(db_file=DB_FILE, table=POSITIONS_TABLE_NAME, field_name='code', field_value=code):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Position with code {code} didn't exists in DB.")

    return f"Position with code {code} deleted"


# Order matters. This method should be at the end of the router for avoiding to override sub-path methods
@router.get("/{code}")
def get_position_details(code: int):
    result = db.query_db(db_file=DB_FILE, table=POSITIONS_TABLE_NAME, fields={"code": code})

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Position with code {code} not found")

    return result[0]
