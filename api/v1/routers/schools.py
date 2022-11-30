from typing import Optional, List

from fastapi import APIRouter, status, Depends
from pydantic import BaseModel
from starlette.responses import JSONResponse

from api.model.generic import GenericMessage, GenericExceptionMessage
from api.model.school import School
from api.utils import db
from api.utils.db import DB_FILE
from api.utils.login import validate_access_token

router = APIRouter()
SCHOOLS_TABLE_NAME = 'schools'


@router.get("", responses={status.HTTP_200_OK: {"model": List[School]}})
def list_schools(name: Optional[str] = None, province: Optional[str] = None,
                 locality: Optional[str] = None):
    fields = {}
    if name:
        fields['name'] = name
    if province:
        fields['province'] = province
    if locality:
        fields['locality'] = locality

    return [School(code=row[0], name=row[1], province=row[2], locality=row[3])
            for row in db.query_db(db_file=DB_FILE, table=SCHOOLS_TABLE_NAME, fields=fields)]


@router.post("", status_code=status.HTTP_201_CREATED,
             responses={status.HTTP_201_CREATED: {"model": GenericMessage},
                        status.HTTP_409_CONFLICT: {"model": GenericExceptionMessage}})
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
        return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                            content={"status_code": status.HTTP_409_CONFLICT,
                                     "detail": f"School with code {code} already exists in DB."})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": f"School with code {code} created"})


@router.put("", responses={status.HTTP_200_OK: {"model": GenericMessage},
                           status.HTTP_400_BAD_REQUEST: {"model": GenericExceptionMessage},
                           status.HTTP_409_CONFLICT: {"model": GenericExceptionMessage}})
def update_school(code: int, name: Optional[str] = None, province: Optional[str] = None,
                  locality: Optional[str] = None):
    if not name and not province and not locality:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status_code": status.HTTP_400_BAD_REQUEST,
                                     "detail": f"No fields to update in School with code {code}, "
                                               f"please provide a new name, province or locality at least."})
    fields = {}
    if name:
        fields['name'] = name
    if province:
        fields['province'] = province
    if locality:
        fields['locality'] = locality

    if not db.update_db(db_file=DB_FILE, table=SCHOOLS_TABLE_NAME, field_id_name='code', field_id_value=code,
                        fields_to_update=fields):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                            content={"status_code": status.HTTP_409_CONFLICT,
                                     "detail": f"Can't update school with code {code}"})

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"School with code {code} updated"})


@router.delete("", dependencies=[Depends(validate_access_token)],
               responses={status.HTTP_200_OK: {"model": GenericMessage},
                          status.HTTP_404_NOT_FOUND: {"model": GenericExceptionMessage},
                          status.HTTP_401_UNAUTHORIZED: {"model": BaseModel}})
def delete_school(code: int):
    if not db.delete_db(db_file=DB_FILE, table=SCHOOLS_TABLE_NAME, field_name='code', field_value=code):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"status_code": status.HTTP_404_NOT_FOUND,
                                     "detail": f"School with code {code} didn't exists in DB."})

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"School with code {code} deleted"})


# Order matters. This method should be at the end of the router for avoiding to override sub-path methods
@router.get("/{code}", responses={status.HTTP_200_OK: {"model": School},
                                  status.HTTP_404_NOT_FOUND: {"model": GenericExceptionMessage}})
def get_school_details(code: int):
    result = db.query_db(db_file=DB_FILE, table=SCHOOLS_TABLE_NAME, fields={"code": code})

    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"status_code": status.HTTP_404_NOT_FOUND,
                                     "detail": f"School with code {code} didn't exists in DB."})

    return School(code=result[0][0], name=result[0][1], province=result[0][2], locality=result[0][3])
