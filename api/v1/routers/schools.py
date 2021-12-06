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

    # TODO if False, insert failed
    return db.insert_db(db_file=DB_FILE, table=SCHOOLS_TABLE_NAME, fields=fields)


# Order matters. This method should be at the end of the router for avoiding to override sub-path methods
@router.get("/{code}")
def get_school_details(code: int):
    result = db.query_db(db_file=DB_FILE, table=SCHOOLS_TABLE_NAME, fields={"code": code})

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=F"School with code {code} not found")

    return result[0]
