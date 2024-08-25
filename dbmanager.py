import psycopg2


class DBManager:

    def get_companies_and_vacancies_count(self, params):
        '''
        Получаем список всех компаний и количество вакансий у каждой компании
        '''
        conn = psycopg2.connect(dbname='courswork5', **params)
        with conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT employers.name, COUNT(vacancies.employer_id) AS vacancies_count 
                FROM employers 
                LEFT JOIN vacancies ON employers.id = vacancies.employer_id 
                GROUP BY employers.name''')
                companies_and_vacs_count = cur.fetchall()
                return companies_and_vacs_count
        conn.close()

    def get_all_vacancies(self, params):
        '''
        Получаем список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        '''
        conn = psycopg2.connect(dbname='courswork5', **params)
        with conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT employers.name, vacancies.name, vacancies.salary, vacancies.url 
                FROM employers JOIN vacancies ON employers.id = vacancies.employer_id ''')
                all_vacancies = cur.fetchall()
                return all_vacancies
        conn.close()

    def get_avg_salary(self, params):
        '''
        Получаем среднюю зарплату по вакансиям
        '''
        conn = psycopg2.connect(dbname='courswork5', **params)
        with conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT ROUND(AVG(salary)) AS salary_avg FROM vacancies''')
                avg_salary = cur.fetchone()[0]
                return avg_salary
        conn.close()

    def get_vacancies_with_higher_salary(self, params):
        '''
        Получаем список всех вакансий, у которых зарплата выше средней по всем вакансиям
        '''
        conn = psycopg2.connect(dbname='courswork5', **params)
        with conn:
            with conn.cursor() as cur:
                cur.execute('''SELECT * FROM vacancies WHERE salary > (select AVG(salary) 
                            FROM vacancies)''')
                vacancies_with_higher_salary = cur.fetchall()
                return vacancies_with_higher_salary
        conn.close()

    def get_vacancies_with_keyword(self, keyword, params):
        '''
        Получаем список всех вакансий, в названии которых содержатся переданные в метод слова
        '''
        conn = psycopg2.connect(dbname='courswork5', **params)
        with conn:
            with conn.cursor() as cur:
                cur.execute(f'''SELECT * FROM vacancies WHERE name ILIKE '%{keyword}%' ''')
                vacancies_with_keyword = cur.fetchall()
                return vacancies_with_keyword

        conn.close()
