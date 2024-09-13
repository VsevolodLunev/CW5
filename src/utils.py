import psycopg2
from typing import Any


def create_database(database_name: str, params: dict) -> None:
    """
    функция для создания Базы Данных и создания таблиц в БД
    """
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id INTEGER,
                employer_name text not null,
                employer_area TEXT not null,
                url TEXT,
                open_vacancies INTEGER,
                
                CONSTRAINT pk_employers_employer_id PRIMARY KEY(employer_id)
            );
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancy (
                vacancy_id INTEGER,
                vacancy_name VARCHAR,
                vacancy_area VARCHAR,
                salary INTEGER,
                employer_id INTEGER,
                vacancy_url VARCHAR,
                
                CONSTRAINT pk_vacancy_vacancy_id PRIMARY KEY(vacancy_id)
            );
            ALTER TABLE vacancy ADD CONSTRAINT fk_vacancy_employers FOREIGN KEY(employer_id) 
            REFERENCES employers(employer_id)
        """)

    conn.commit()
    conn.close()


def save_data_to_database_emp(data_emp: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """
    Функция для заполнения таблицы компаний в БД
    """
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for emp in data_emp:
            cur.execute("""
                INSERT INTO employers (employer_id, employer_name, employer_area, url, open_vacancies)
                VALUES (%s, %s, %s, %s, %s)
                """,
                        (emp['id'], emp['name'], emp['area']['name'], emp['alternate_url'], emp['open_vacancies']))

    conn.commit()
    conn.close()


def save_data_to_database_vac(data_vac: list[dict[str, Any]], database_name: str, params: dict) -> None:
    """
    Функция для заполнения таблицы вакансий в БД
    """

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for vac in data_vac:
            if vac['salary'] is None or vac['salary']['from'] is None:
                cur.execute("""
                   INSERT INTO vacancy (vacancy_id, vacancy_name, vacancy_area, salary, employer_id, vacancy_url)
                   VALUES (%s, %s, %s, %s, %s, %s)
                   """,
                            (vac.get('id'), vac['name'], vac['area']['name'], 0, vac['employer']['id'],
                             vac['alternate_url']))
            else:
                cur.execute("""
                    INSERT INTO vacancy (vacancy_id, vacancy_name, vacancy_area, salary, employer_id, vacancy_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                            (vac.get('id'), vac['name'], vac['area']['name'], vac['salary']['from'],
                             vac['employer']['id'], vac['alternate_url']))

    conn.commit()
    conn.close()
