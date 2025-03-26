import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any


class FileHandler(ABC):
    @abstractmethod
    def get_data(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def add_data(self, data: List['Vacancy']) -> None:
        pass

    @abstractmethod
    def delete_data(self, criteria: Dict[str, Any]) -> None:
        pass


class JSONFileHandler(FileHandler):
    def __init__(self, filename: str = "vacancies.json"):
        # Определяем путь к корню проекта
        project_root = Path(__file__).parent.parent

        # Создаем путь к папке data
        self.__data_dir = project_root / "data"
        self.__data_dir.mkdir(exist_ok=True)  # Создаем папку если не существует

        # Полный путь к файлу
        self.__filename = self.__data_dir / filename
        self.__ensure_file_exists()

    def __ensure_file_exists(self) -> None:
        """Создает файл если он не существует"""
        self.__filename.touch(exist_ok=True)

    @staticmethod
    def __vacancy_to_dict(vacancy: 'Vacancy') -> Dict[str, Any]:
        return {
            "title": vacancy.title,
            "company": vacancy.company,
            "salary_min": vacancy.salary_min,
            "salary_max": vacancy.salary_max,
            "link": vacancy.link
        }

    def get_data(self) -> List[Dict[str, Any]]:
        try:
            with open(self.__filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def __is_duplicate(self, existing_data: List[Dict[str, Any]], new_item: Dict[str, Any]) -> bool:
        return any(item['link'] == new_item['link'] for item in existing_data)

    def add_data(self, data: List['Vacancy']) -> None:
        # Преобразуем объекты Vacancy в словари
        new_data = [self.__vacancy_to_dict(v) for v in data]

        # Получаем существующие данные
        existing_data = self.get_data()

        # Фильтруем дубликаты
        filtered_new_data = [
            item for item in new_data
            if not self.__is_duplicate(existing_data, item)
        ]

        # Объединяем данные
        combined_data = existing_data + filtered_new_data

        # Сохраняем в файл
        with open(self.__filename, "w", encoding="utf-8") as file:
            json.dump(combined_data, file, ensure_ascii=False, indent=4)

    def delete_data(self, criteria: Dict[str, Any]) -> None:
        data = self.get_data()
        filtered_data = [
            item for item in data
            if not all(
                str(item.get(key)) == str(value)
                for key, value in criteria.items()
            )
        ]

        with open(self.__filename, "w", encoding="utf-8") as file:
            json.dump(filtered_data, file, ensure_ascii=False, indent=4)