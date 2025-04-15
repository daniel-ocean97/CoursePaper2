import json
import os

import pytest

from src.vacancies import Vacancy
from src.work_with_files import \
    JSONFileHandler  # Замените your_module на имя файла


@pytest.fixture
def temp_file(tmp_path):
    file = tmp_path / "test_vacancies.json"
    yield str(file)
    if os.path.exists(file):
        os.remove(file)


@pytest.fixture
def sample_vacancies():
    return [
        Vacancy("Python Developer", "Company A", 100000, "https://example.com/1"),
        Vacancy("Java Developer", "Company B", "80000-120000", "https://example.com/2"),
        Vacancy(
            "Data Scientist",
            "Company C",
            {"from": 150000, "to": 200000},
            "https://example.com/3",
        ),
    ]


def test_add_and_get_data(temp_file, sample_vacancies):
    handler = JSONFileHandler(temp_file)

    # Добавляем вакансии
    handler.add_data(sample_vacancies)

    # Проверяем получение данных
    data = handler.get_data()
    assert len(data) == 3
    assert data[0]["title"] == "Python Developer"
    assert data[1]["salary_min"] == 80000
    assert data[2]["link"] == "https://example.com/3"


def test_duplicate_handling(temp_file, sample_vacancies):
    handler = JSONFileHandler(temp_file)

    # Добавляем одни и те же данные дважды
    handler.add_data(sample_vacancies)
    handler.add_data(sample_vacancies)

    data = handler.get_data()
    assert len(data) == 3  # Дубликаты не должны добавиться


def test_delete_data(temp_file, sample_vacancies):
    handler = JSONFileHandler(temp_file)
    handler.add_data(sample_vacancies)

    # Удаляем по критерию
    handler.delete_data({"link": "https://example.com/2"})
    data = handler.get_data()
    assert len(data) == 2
    assert all(item["link"] != "https://example.com/2" for item in data)


def test_complex_criteria(temp_file, sample_vacancies):
    handler = JSONFileHandler(temp_file)
    handler.add_data(sample_vacancies)

    # Удаляем по нескольким критериям
    handler.delete_data({"company": "Company A", "salary_min": 100000})
    data = handler.get_data()
    assert len(data) == 2


def test_empty_file_handling(temp_file):
    handler = JSONFileHandler(temp_file)
    data = handler.get_data()
    assert data == []


def test_partial_update(temp_file, sample_vacancies):
    handler = JSONFileHandler(temp_file)

    # Первое добавление
    handler.add_data(sample_vacancies[:2])
    assert len(handler.get_data()) == 2

    # Второе добавление
    handler.add_data(sample_vacancies[2:])
    assert len(handler.get_data()) == 3


def test_invalid_data_handling(temp_file):
    handler = JSONFileHandler(temp_file)

    # Создаем файл с невалидным JSON
    with open(temp_file, "w") as f:
        f.write("invalid json")

    data = handler.get_data()
    assert data == []



def test_delete_nonexistent_data(temp_file, sample_vacancies):
    handler = JSONFileHandler(temp_file)
    handler.add_data(sample_vacancies)

    # Пытаемся удалить несуществующие данные
    handler.delete_data({"link": "https://nonexistent.com"})
    data = handler.get_data()
    assert len(data) == 3
