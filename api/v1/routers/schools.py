from typing import Optional

from fastapi import APIRouter, HTTPException, status

from api.utils import db
from api.utils.db import DB_FILE

router = APIRouter()
SCHOOLS_TABLE_NAME = 'schools'


@router.get("")
def list_schools(name: Optional[str] = None, province: Optional[str] = None,
                 locality: Optional[str] = None):
    fields = {}
    if name:
        fields['name'] = name
    if province:
        fields['province'] = province
    if locality:
        fields['locality'] = locality

    return db.query_db(db_file=DB_FILE, table=SCHOOLS_TABLE_NAME, fields=fields)


@router.post("")
def insert_school(code: int, name: str, province: str, locality: str):
    fields = {}
    if code:
        fields['code'] = code
    if name:
        fields['name'] = name
    if province:
        fields['province'] = province
    if locality:
        fields['locality'] = locality

    if not db.insert_db(db_file=DB_FILE, table=SCHOOLS_TABLE_NAME, fields=fields):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"School with code {code} already exists in DB.")

    return f"School with code {code} created"


@router.put("")
def update_school(code: int, name: Optional[str] = None, province: Optional[str] = None,
                  locality: Optional[str] = None):
    if not name and not province and not locality:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"No fields to update in School with code {code}, "
                                   f"please provide a new name, province or locality at least.")
    fields = {}
    if name:
        fields['name'] = name
    if province:
        fields['province'] = province
    if locality:
        fields['locality'] = locality

    if not db.update_db(db_file=DB_FILE, table=SCHOOLS_TABLE_NAME, field_id_name='code', field_id_value=code,
                        fields_to_update=fields):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Can't update school with code {code}")

    return f"School with code {code} updated"


@router.delete("")
def delete_school(code: int):
    if not db.delete_db(db_file=DB_FILE, table=SCHOOLS_TABLE_NAME, field_name='code', field_value=code):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"School with code {code} didn't exists in DB.")

    return f"School with code {code} deleted"


# Order matters. This method should be at the end of the router for avoiding to override sub-path methods
@router.get("/{code}")
def get_school_details(code: int):
    result = db.query_db(db_file=DB_FILE, table=SCHOOLS_TABLE_NAME, fields={"code": code})

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"School with code {code} not found")

    return result[0]
