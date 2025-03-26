from src.external_api import HHAPI
from src.vacancies import Vacancy
from src.work_with_files import JSONFileHandler

#  Создание экземпляра класса для работы с API

hh_api = HHAPI()


def user_interaction():
    user_request = input("Введите поисковой запрос\n")
    result = hh_api.load_vacancies(user_request)
    result = Vacancy.cast_to_object(result)
    sort_request = input("Отсортировать вакансии по зарплате? (от большей к меньшей)\n")
    if sort_request.lower() == "да":
        sorted(result, reverse=True)
    file_request = input("Если хотите записать результат в файл напишите 'файл'\n")
    if file_request.lower() == "файл":
        filename = input("Укажите имя файла. (В конце обязательно '.json')\n")
        filehandler = JSONFileHandler(filename)
        filehandler.add_data(result)
    else:
        filehandler1 = JSONFileHandler()
        for vacancy in result:
            print(filehandler1.vacancy_to_dict(vacancy))


if __name__ == "__main__":
    user_interaction()
