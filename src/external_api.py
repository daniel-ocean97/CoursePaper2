from abc import ABC, abstractmethod
import requests
from typing import Any, Dict, List


class JobAPI(ABC):
    """Абстрактный класс для работы с API вакансий"""

    @abstractmethod
    def connect(self) -> None:
        """Метод для установки соединения с API"""
        pass

    @abstractmethod
    def load_vacancies(self, keyword: str, *args: Any, **kwargs: Any) -> List[Dict[str, Any]]:
        """Метод для получения вакансий по ключевому слову"""
        pass


class HHAPI(JobAPI):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self):
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100}
        self.__vacancies = []
        self.__connected = False
        self.__session = requests.Session()

    def connect(self):
        """Публичный метод для реализации абстрактного класса"""
        self.__establish_connection()

    def __establish_connection(self):
        """Приватный метод для реального подключения"""
        try:
            response = self.__session.get(
                f"{self.__url}",
                headers=self.__headers
            )
            response.raise_for_status()
            self.__connected = True
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ошибка подключения: {e}")

    def load_vacancies(self, keyword: str, *args: Any, **kwargs: Any) -> List[Dict[str, Any]]:
        """ Метод для получения вакансий """
        if not self.__connected:
            self.__establish_connection()
        self.__params['text'] = keyword
        for page in range(20):
            self.__params['page'] = page
            response: requests.Response = self.__session.get(
                self.__url,
                headers=self.__headers,
                params=self.__params
            )
            temp_vacancies: List[Dict[str, Any]] = response.json()['items']
            self.__vacancies.extend(temp_vacancies)

            if not temp_vacancies:  # Прерываем если закончились вакансии
                break
        return self.__vacancies

# Пример использования
if __name__ == "__main__":
    hh = HHAPI()

    vacancies = hh.load_vacancies(keyword="Официант")

    print(f"Найдено вакансий: {len(vacancies)}")
    for v in vacancies[:3]:
        print(v)