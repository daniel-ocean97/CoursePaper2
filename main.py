from src.external_api import HHAPI
from src.vacancies import Vacancy
from src.work_with_files import JSONFileHandler


print("Загружаю вакансии")
hh_api = HHAPI()
hh_vacancies = hh_api.load_vacancies(keyword="Python")[0:100]
print("Создаём 100 экземпляров класса Vacancy")
vacancies_data = Vacancy.cast_to_object(hh_vacancies)
json_file_handler = JSONFileHandler()
print("Фильтрую по зарплате")
vacancies_data = sorted(vacancies_data, reverse=True)
print("Записываем их в файл")
json_file_handler.add_data(vacancies_data)