import psycopg2


class DBManager:
    """Класс, который подключается к БД PostgreSQL."""
    def __init__(self, database_name, params):
        self.dbname = database_name
        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> list:
        """получает список всех компаний и количество вакансий у каждой компании."""
        self.cur.execute("""
        SELECT companies.company_name, COUNT(vacancies.company_id)
        FROM companies
        JOIN vacancies USING (company_id)
        GROUP BY companies.company_name
        ORDER BY COUNT DESC
        """)
        return self.cur.fetchall()

    def get_all_vacancies(self) -> list:
        """получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансии."""
        self.cur.execute("""
        SELECT companies.company_name, job_title, salary_from, link_to_vacancy
        FROM vacancies
        JOIN companies USING (company_id)
        ORDER BY salary_from DESC
        """)
        return self.cur.fetchall()

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        self.cur.execute("""
        SELECT AVG(salary_from) FROM vacancies""")
        rows = self.cur.fetchall()
        return rows if rows else None

    def get_vacancies_with_higher_salary(self) -> list:
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        self.cur.execute("""
        SELECT job_title, salary_from FROM vacancies 
        WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)""")
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword) -> list:
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        q = """SELECT * FROM vacancies
                WHERE LOWER(job_title) LIKE %s
        """
        self.cur.execute(q, ('%' + keyword.lower() + '%',))
        return self.cur.fetchall()
