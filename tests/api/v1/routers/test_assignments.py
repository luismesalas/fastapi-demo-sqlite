from fastapi.testclient import TestClient
from starlette import status

import main
from api.utils.db import DB_FILE

client = TestClient(main.get_app())
assignments_path = "/api/v1/assignments"


def test_get_positions_in_a_school_200(mocker):
    # Given
    school_code_param = 777777
    query_result = [(41009950, '00597036', 14, '00597036', 'PEDAGOGÍA TERAPÉUTICA', 'MAESTROS'),
                    (41009950, '00597037', 1, '00597037', 'AUDICIÓN Y LENGUAJE', 'MAESTROS')]
    db_query_inner_join_mock = mocker.patch('api.v1.routers.assignments.db.query_inner_join', return_value=query_result)

    # When
    response = client.get(f"{assignments_path}/positions-in-a-school?school_code={school_code_param}")

    # Then
    db_query_inner_join_mock.assert_called_once_with(db_file=DB_FILE, table_left='assignments', table_right='positions',
                                                     field_key_left='position', field_key_right='code',
                                                     field_filters_left={'school': school_code_param},
                                                     field_filters_right={})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"position": {"code": "00597036", "name": "PEDAGOGÍA TERAPÉUTICA", "corps": "MAESTROS"}, "quantity": 14},
        {"position": {"code": "00597037", "name": "AUDICIÓN Y LENGUAJE", "corps": "MAESTROS"}, "quantity": 1}]


def test_get_schools_with_a_position_200(mocker):
    # Given
    position_param = "PI591201"
    query_result = [(14700377, 'PI591201', 1, 14700377, 'I.E.S. CARMEN PANTIÓN', 'CÓRDOBA', 'PRIEGO DE CÓRDOBA'),
                    (29006568, 'PI591201', 1, 29006568, 'I.E.S. LOS MANANTIALES', 'MÁLAGA', 'TORREMOLINOS')]
    db_query_inner_join_mock = mocker.patch('api.v1.routers.assignments.db.query_inner_join', return_value=query_result)

    # When
    response = client.get(f"{assignments_path}/schools-with-a-position?position_code={position_param}")

    # Then
    db_query_inner_join_mock.assert_called_once_with(db_file=DB_FILE, table_left='assignments', table_right='schools',
                                                     field_key_left='school', field_key_right='code',
                                                     field_filters_left={'position': position_param},
                                                     field_filters_right={})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"school": {"code": 14700377, "name": "I.E.S. CARMEN PANTIÓN", "province": "CÓRDOBA",
                                           "locality": "PRIEGO DE CÓRDOBA"}, "quantity": 1},
                               {"school": {"code": 29006568, "name": "I.E.S. LOS MANANTIALES", "province": "MÁLAGA",
                                           "locality": "TORREMOLINOS"}, "quantity": 1}]
