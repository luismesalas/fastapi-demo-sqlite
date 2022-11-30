from typing import Optional, List

from fastapi import APIRouter, status, Depends
from pydantic import BaseModel
from starlette.responses import JSONResponse

from api.model.generic import GenericMessage, GenericExceptionMessage
from api.model.position import Position
from api.utils import db
from api.utils.db import DB_FILE
from api.utils.login import validate_access_token

router = APIRouter()
POSITIONS_TABLE_NAME = 'positions'


@router.get("", responses={status.HTTP_200_OK: {"model": List[Position]}})
def list_positions(name: Optional[str] = None, corps: Optional[str] = None):
    fields = {}
    if name:
        fields['name'] = name
    if corps:
        fields['corps'] = corps

    return [Position(code=row[0], name=row[1], corps=row[2])
            for row in db.query_db(db_file=DB_FILE, table=POSITIONS_TABLE_NAME, fields=fields)]


@router.post("", status_code=status.HTTP_201_CREATED,
             responses={status.HTTP_201_CREATED: {"model": GenericMessage},
                        status.HTTP_409_CONFLICT: {"model": GenericExceptionMessage}})
def insert_position(code: str, name: str, corps: str):
    fields = {}
    if code:
        fields['code'] = code
    if name:
        fields['name'] = name
    if corps:
        fields['corps'] = corps

    if not db.insert_db(db_file=DB_FILE, table=POSITIONS_TABLE_NAME, fields=fields):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                            content={"status_code": status.HTTP_409_CONFLICT,
                                     "detail": f"Position with code {code} already exists in DB."})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": f"Position with code {code} created"})


@router.put("", responses={status.HTTP_200_OK: {"model": GenericMessage},
                           status.HTTP_400_BAD_REQUEST: {"model": GenericExceptionMessage},
                           status.HTTP_409_CONFLICT: {"model": GenericExceptionMessage}})
def update_position(code: str, name: Optional[str] = None, corps: Optional[str] = None):
    if not name and not corps:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"status_code": status.HTTP_400_BAD_REQUEST,
                                     "detail": f"No fields to update in position with code {code}, "
                                               f"please provide a new name, corps or locality at least."})
    fields = {}
    if name:
        fields['name'] = name
    if corps:
        fields['corps'] = corps

    if not db.update_db(db_file=DB_FILE, table=POSITIONS_TABLE_NAME, field_id_name='code', field_id_value=code,
                        fields_to_update=fields):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                            content={"status_code": status.HTTP_409_CONFLICT,
                                     "detail": f"Can't update position with code {code}"})

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"Position with code {code} updated"})


@router.delete("", dependencies=[Depends(validate_access_token)],
               responses={status.HTTP_200_OK: {"model": GenericMessage},
                          status.HTTP_404_NOT_FOUND: {"model": GenericExceptionMessage},
                          status.HTTP_401_UNAUTHORIZED: {"model": BaseModel}})
def delete_position(code: str):
    if not db.delete_db(db_file=DB_FILE, table=POSITIONS_TABLE_NAME, field_name='code', field_value=code):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"status_code": status.HTTP_404_NOT_FOUND,
                                     "detail": f"Position with code {code} didn't exists in DB."})

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"Position with code {code} deleted"})


# Order matters. This method should be at the end of the router for avoiding to override sub-path methods
@router.get("/{code}", responses={status.HTTP_200_OK: {"model": Position},
                                  status.HTTP_404_NOT_FOUND: {"model": GenericExceptionMessage}})
def get_position_details(code: str):
    result = db.query_db(db_file=DB_FILE, table=POSITIONS_TABLE_NAME, fields={"code": code})

    if not result:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"status_code": status.HTTP_404_NOT_FOUND,
                                     "detail": f"Position with code {code} didn't exists in DB."})

    return Position(code=result[0][0], name=result[0][1], corps=result[0][2])
