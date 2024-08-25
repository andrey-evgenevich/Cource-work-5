import requests


class HHParser:
    """
    Создаем класс для подключения к HH и получения данных по компаниям и вакансиям
    """

    def __init__(self, list_id):
        self.list_id = list_id

    def job_employers(self, ids):
        url = f'https://api.hh.ru/employers/{ids}/'
        params = {'per_page': 10, "sort_by": "by_vacancies_open", 'area': 4}
        response = requests.get(url, params=params)
        employer = response.json()
        return {
            'id': employer['id'],
            'name': employer['name'],
            'url': employer['alternate_url']
        }

    def job_vacancies(self, ids):
        """
        Подключаемся
        """
        url = 'https://api.hh.ru/vacancies/'
        params = {"per_page": 10, "employer_id": ids, "area": 4}
        response = requests.get(url, params=params)
        vacancies = response.json()['items']
        return vacancies

    def get_employers_list(self):
        """
        Получаем данные о компаниях
        """
        employers_list = []

        for ids in self.list_id:
            employers_list.append(self.job_employers(ids))
        return employers_list

    def get_vacancies_list(self):
        """
        Получаем данные о вакансиях
        """
        emp = self.get_employers_list()
        vacancies_list = []
        for employer in emp:
            vacancies_list.extend(self.job_vacancies(employer["id"]))
        return vacancies_list

    def filter_salary(self):
        """
        Готовим данные по вакансиям для таблицы
        """
        vacancies = self.get_vacancies_list()
        filter_vacancies = []
        for vac in vacancies:
            if not vac["salary"]:
                vac["salary"] = 0
                vac["currency"] = "Валюта не определена"
            else:
                if vac["salary"] is None:
                    vac["salary"] = 0
                else:
                    if vac["salary"]["currency"]:
                        vac["currency"] = vac["salary"]["currency"]
                    else:
                        vac["currency"] = "Валюта не определена"
                    if vac["salary"]["from"] is None and vac["salary"]["to"] is None:
                        vac["salary"] = 0
                    else:
                        if vac["salary"]["from"] is None and vac["salary"]["to"] is not None:
                            vac["salary"] = vac["salary"]["to"]
                        else:
                            if vac["salary"]["from"] is not None and vac["salary"]["to"] is None:
                                vac["salary"] = vac["salary"]["from"]
                            else:
                                if vac["salary"]["from"] is not None and vac["salary"]["to"] is not None:
                                    vac["salary"] = vac["salary"]["to"]
            filter_vacancies.append({
                "id": vac["id"],
                "name": vac["name"],
                "salary": vac["salary"],
                "currency": vac["currency"],
                "url": vac["alternate_url"],
                "employer": vac["employer"]["id"],
            })
        return filter_vacancies
