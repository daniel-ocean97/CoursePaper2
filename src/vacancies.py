from typing import Optional, Union, Dict
from urllib.parse import urlparse


class Vacancy:
    __slots__ = ('title', 'company', 'salary_min', 'salary_max', 'link')

    def __init__(
            self,
            title: str,
            company: str,
            salary: Optional[Union[int, str, Dict[str, int]]] = None,
            link: str = ''
    ):
        self.title = title
        self.company = company
        self.link = link

        # Валидация и парсинг зарплаты
        self.salary_min, self.salary_max = self.__validate_salary(salary)

        # Вызов валидаторов
        self.__validate_title()
        self.__validate_company()
        self.__validate_link()

    def __validate_title(self) -> None:
        if not isinstance(self.title, str) or len(self.title.strip()) == 0:
            raise ValueError("Некорректное название вакансии")

    def __validate_company(self) -> None:
        if not isinstance(self.company, str) or len(self.company.strip()) == 0:
            raise ValueError("Некорректное название компании")

    def __validate_salary(
            self,
            salary: Optional[Union[int, str, Dict[str, int]]]
    ) -> tuple[Optional[int], Optional[int]]:
        if salary is None:
            return (None, None)

        if isinstance(salary, int):
            return (salary, salary)

        if isinstance(salary, str):
            try:
                parts = list(map(int, salary.split('-')))
                return (parts[0], parts[1]) if len(parts) > 1 else (parts[0], parts[0])
            except:
                raise ValueError("Некорректный формат зарплаты")

        if isinstance(salary, dict):
            return (salary.get('from'), salary.get('to'))

        raise ValueError("Неподдерживаемый формат зарплаты")

    def __validate_link(self) -> None:
        if self.link:
            result = urlparse(self.link)
            if not all([result.scheme in ('http', 'https'), result.netloc]):
                raise ValueError("Некорректная ссылка")

    # Методы сравнения
    def __get_comparable_salary(self) -> int:
        return self.salary_min or self.salary_max or 0

    def __eq__(self, other: 'Vacancy') -> bool:
        return self.__get_comparable_salary() == other.__get_comparable_salary()

    def __lt__(self, other: 'Vacancy') -> bool:
        return self.__get_comparable_salary() < other.__get_comparable_salary()

    def __le__(self, other: 'Vacancy') -> bool:
        return self.__get_comparable_salary() <= other.__get_comparable_salary()

    def __gt__(self, other: 'Vacancy') -> bool:
        return self.__get_comparable_salary() > other.__get_comparable_salary()

    def __ge__(self, other: 'Vacancy') -> bool:
        return self.__get_comparable_salary() >= other.__get_comparable_salary()

    def __repr__(self) -> str:
        return f"Vacancy({self.title}, {self.company}, {self.salary_min}-{self.salary_max})"


    @classmethod
    def cast_to_object(cls, vacancies_data: list[dict]) -> list['Vacancy']:
        """
        Преобразует сырые данные из API в список объектов Vacancy
        """
        vacancies = []

        for vacancy_data in vacancies_data:
            try:
                # Извлекаем основные данные
                title = vacancy_data.get('name', '')
                company = vacancy_data.get('employer', {}).get('name', '')
                link = vacancy_data.get('alternate_url', '')

                # Обрабатываем зарплату
                salary_data = vacancy_data.get('salary')
                salary = None

                if salary_data:
                    # Приводим к единому формату для нашего класса
                    salary = {
                        'from': salary_data.get('from'),
                        'to': salary_data.get('to')
                    }

                # Создаем объект вакансии
                vacancy = cls(
                    title=title,
                    company=company,
                    salary=salary,
                    link=link
                )

                vacancies.append(vacancy)

            except (KeyError, ValueError) as e:
                print(f"Ошибка обработки вакансии: {e}")
                continue

        return vacancies