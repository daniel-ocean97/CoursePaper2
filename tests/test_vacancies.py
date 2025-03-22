import pytest
from src.vacancies import Vacancy


# Фикстуры для тестовых данных
@pytest.fixture
def sample_vacancies():
    return [
        Vacancy("Python Dev", "Company A", 100000, "https://company.com"),
        Vacancy("Java Dev", "Company B", "80000-120000"),
        Vacancy("Data Scientist", "Company C", {"from": 150000, "to": 200000}),
        Vacancy("Frontend Dev", "Company D", link="http://example.org"),
    ]


@pytest.fixture
def raw_api_data():
    return [
        {
            "name": "Backend Developer",
            "employer": {"name": "Tech Corp"},
            "salary": {"from": 120000, "to": 180000},
            "alternate_url": "https://techcorp.com/jobs/1"
        },
        {
            "name": "",  # Invalid title
            "employer": {"name": "Bad Company"},
            "salary": None,
            "alternate_url": ""
        }
    ]


# Тесты инициализации и валидации
def test_valid_vacancy_creation():
    vacancy = Vacancy("Valid", "Company", 100000)
    assert vacancy.title == "Valid"
    assert vacancy.company == "Company"
    assert vacancy.salary_min == 100000
    assert vacancy.salary_max == 100000


def test_invalid_title():
    with pytest.raises(ValueError):
        Vacancy("", "Company", 50000)
    with pytest.raises(ValueError):
        Vacancy(123, "Company", 50000)


def test_salary_parsing():
    # Зарплата в виде числа
    v = Vacancy("Title", "Co", 50000)
    assert v.salary_min == v.salary_max == 50000

    # Зарплата в виде строки
    v = Vacancy("Title", "Co", "70000-90000")
    assert v.salary_min == 70000
    assert v.salary_max == 90000

    # Зарплата в виде словаря
    v = Vacancy("Title", "Co", {"from": 80000, "to": 100000})
    assert v.salary_min == 80000
    assert v.salary_max == 100000

    # Некорректный тип зарплаты
    with pytest.raises(ValueError):
        Vacancy("Title", "Co", "invalid-salary")


def test_link_validation():
    # Valid links
    Vacancy("T", "C", link="https://valid.com")
    Vacancy("T", "C", link="http://example.ru/path")

    # Invalid links
    with pytest.raises(ValueError):
        Vacancy("T", "C", link="ftp://invalid.com")
    with pytest.raises(ValueError):
        Vacancy("T", "C", link="invalid-url")


# Тесты сравнения
def test_comparison_operators():
    v1 = Vacancy("A", "Co", 100000)
    v2 = Vacancy("B", "Co", 150000)
    v3 = Vacancy("C", "Co", "90000-110000")
    v4 = Vacancy("D", "Co", None)

    assert v2 > v1
    assert v1 > v3
    assert v3 <= v1
    assert v1 == Vacancy("X", "Y", 100000)
    assert v4 < v1  # None считается как 0


# Тесты преобразования из API данных
def test_cast_to_object(raw_api_data):
    vacancies = Vacancy.cast_to_object(raw_api_data)
    assert len(vacancies) == 1  # Одна валидная вакансия

    valid_vacancy = vacancies[0]
    assert valid_vacancy.title == "Backend Developer"
    assert valid_vacancy.company == "Tech Corp"
    assert valid_vacancy.salary_min == 120000
    assert valid_vacancy.link == "https://techcorp.com/jobs/1"


def test_invalid_data_handling(capsys, raw_api_data):
    vacancies = Vacancy.cast_to_object(raw_api_data)
    captured = capsys.readouterr()
    assert "Ошибка обработки вакансии" in captured.out


# Тесты дополнительных функций
def test_repr():
    v = Vacancy("Dev", "Co", 100000)
    assert "Dev" in repr(v)
    assert "Co" in repr(v)
    assert "100000" in repr(v)


def test_slots_enforcement():
    v = Vacancy("T", "C", 50000)
    with pytest.raises(AttributeError):
        v.new_attribute = 123