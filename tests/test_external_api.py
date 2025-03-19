import pytest
import requests
from requests.exceptions import RequestException
from unittest.mock import Mock, patch
from src.external_api import HHAPI, JobAPI

@pytest.fixture
def hh_api():
    return HHAPI()


def test_hhapi_initialization(hh_api):
    assert hasattr(hh_api, "_HHAPI__url")
    assert hasattr(hh_api, "_HHAPI__headers")
    assert hasattr(hh_api, "_HHAPI__params")
    assert hh_api._HHAPI__url == 'https://api.hh.ru/vacancies'
    assert isinstance(hh_api._HHAPI__session, requests.Session)


def test_connect_success(hh_api, mocker):
    mock_get = mocker.patch.object(hh_api._HHAPI__session, 'get')
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    hh_api.connect()

    assert hh_api._HHAPI__connected is True
    mock_get.assert_called_once_with(hh_api._HHAPI__url, headers=hh_api._HHAPI__headers)


def test_connect_failure(hh_api, mocker):
    mock_get = mocker.patch.object(hh_api._HHAPI__session, 'get')
    mock_get.side_effect = RequestException("Connection error")

    with pytest.raises(ConnectionError):
        hh_api.connect()

    assert hh_api._HHAPI__connected is False


@patch.object(requests.Session, 'get')
def test_load_vacancies_success(mock_get, hh_api):
    # Настраиваем моки
    mock_response = Mock()
    mock_response.json.return_value = {'items': [{'id': '1'}, {'id': '2'}]}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Вызываем метод
    result = hh_api.load_vacancies("Python")

    # Проверяем результаты
    assert len(result) == 40  # 2 items per page * 20 pages
    assert isinstance(result, list)
    assert all(isinstance(item, dict) for item in result)

    # Проверяем параметры запроса
    expected_params = {
        'text': 'Python',
        'page': 19,  # Последняя страница
        'per_page': 100,
    }
    mock_get.assert_called_with(
        hh_api._HHAPI__url,
        headers=hh_api._HHAPI__headers,
        params=expected_params
    )


def test_load_vacancies_empty_response(hh_api, mocker):
    mock_get = mocker.patch.object(hh_api._HHAPI__session, 'get')
    mock_response = Mock()
    mock_response.json.return_value = {'items': []}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = hh_api.load_vacancies("Empty")

    assert len(result) == 0



