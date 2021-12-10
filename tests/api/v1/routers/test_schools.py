from fastapi.testclient import TestClient
from starlette import status

import main
from api.utils.db import DB_FILE

client = TestClient(main.get_app())

schools_path_v1 = "/api/v1/schools"


def test_get_list_schools_without_params_gets_200(mocker):
    # Given
    query_result = [(4000018, 'C.E.I.P. JOAQUÍN TENA SICILIA', 'ALMERÍA', 'ABLA'),
                    (4000021, 'C.E.I.P. ANTONIO RELAÑO', 'ALMERÍA', 'ABRUCENA'),
                    (4602079, 'C.E.I.P. ABDERA', 'ALMERÍA', 'ADRA')]
    db_query_mock = mocker.patch('api.v1.routers.assignments.db.query_db', return_value=query_result)

    # When
    response = client.get(f"{schools_path_v1}")

    # Then
    db_query_mock.assert_called_once_with(db_file=DB_FILE, table='schools', fields={})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {'code': 4000018, 'name': 'C.E.I.P. JOAQUÍN TENA SICILIA', 'province': 'ABLA', 'locality': 'ALMERÍA'},
        {'code': 4000021, 'name': 'C.E.I.P. ANTONIO RELAÑO', 'province': 'ABRUCENA', 'locality': 'ALMERÍA'},
        {'code': 4602079, 'name': 'C.E.I.P. ABDERA', 'province': 'ADRA', 'locality': 'ALMERÍA'}]


def test_get_list_schools_with_all_params_gets_200(mocker):
    # Given
    school_name_param = 'C.E.I.P FEDERICO GARCÍA LORCA'
    province_param = 'SEVILLA'
    locality_param = 'DOS HERMANAS'
    query_result = [(41009172, 'C.E.I.P. FEDERICO GARCÍA LORCA', 'SEVILLA', 'DOS HERMANAS')]
    db_query_mock = mocker.patch('api.v1.routers.assignments.db.query_db', return_value=query_result)

    # When
    response = client.get(f"{schools_path_v1}?name={school_name_param}"
                          f"&province={province_param}&locality={locality_param}'")

    # Then
    db_query_mock.assert_called_once_with(db_file=DB_FILE, table='schools',
                                          fields={'locality': "DOS HERMANAS'",
                                                  'name': 'C.E.I.P FEDERICO GARCÍA LORCA', 'province': 'SEVILLA'})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {'code': 41009172, 'name': 'C.E.I.P. FEDERICO GARCÍA LORCA', 'province': 'DOS HERMANAS', 'locality': 'SEVILLA'}]
