from config import config
from parser import HHParser
from utils import create_database, creating_tables, data_entry
from dbmanager import DBManager
from settings import list_id


def main():
    print('Подготавливаем данные для таблиц')
    hh = HHParser(list_id)
    hh.get_employers_list()
    hh.filter_salary()
    params = config()
    print('Создаем базу данных')
    create_database(params)
    print('Создаем таблицы')
    creating_tables(params)
    print('Заполняем таблицы')
    data_entry(params, list_id)
    dbm = DBManager()
    print('Теперь Вы можете получить')
    choice = input('1 - список всех компаний и кол-во вакансий у каждой компании\n'
                   '2 - список всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки на вакансию\n'
                   '3 - среднюю зарплату по вакансиям\n'
                   '4 - список всех вакансий, у которых зарплата выше средней по всем вакансиям\n'
                   '"ключевое слово" - список вакансий, в названии которых содержится ключевое слово\n')
    if choice == '1':
        print(dbm.get_companies_and_vacancies_count(params))
    elif choice == '2':
        print(dbm.get_all_vacancies(params))
    elif choice == '3':
        print(dbm.get_avg_salary(params))
    elif choice == '4':
        print(dbm.get_vacancies_with_higher_salary(params))
    else:
        print(dbm.get_vacancies_with_keyword(choice, params))


if __name__ == '__main__':
    main()
