import os
from typing import Dict, List, Optional

import psycopg2
from dotenv import load_dotenv

from src.get_vacancies import get_employers, get_vacancies


def create_database():
    load_dotenv()

    password = os.getenv("DATABASE_PASSWORD")
    host = "localhost"
    port = "5432"
    user = "postgres"
    database = "postgres"

    conn = psycopg2.connect(
        host=host, port=port, user=user, password=password, database=database
    )
    conn.autocommit = True

    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname = 'vacancies';")
    exists = cur.fetchone()
    try:
        if not exists:
            cur.execute("CREATE DATABASE vacancies")
            print("База данных vacancies успешно создана.")
    except Exception:
        print("Не удалось создать базу данных")
    finally:
        cur.close()
        conn.close()

    # print('Не получилось создать базу данных')


def employers_to_table(employers: List[dict[str, Optional[str]]]):
    """Функция, добавляющая работодателей в таблицу"""
    create_database()
    load_dotenv()
    password = os.getenv("DATABASE_PASSWORD")
    conn_params = {
        "host": "localhost",
        "database": "vacancies",
        "user": "postgres",
        "password": password,
    }

    with psycopg2.connect(**conn_params) as conn:  # type: ignore
        with conn.cursor() as cur:
            try:
                cur.execute("DROP TABLE IF EXISTS employers CASCADE;")
                cur.execute(
                    "CREATE TABLE employers (employer varchar(100) PRIMARY KEY not null,"
                    "open_vacancies varchar(100))"
                )

                for employer in employers:
                    name_employer = employer["name"]
                    open_vacancies = employer["open_vacancies"]
                    cur.execute(
                        "INSERT INTO employers VALUES (%s, %s)",
                        (name_employer, open_vacancies),
                    )

                return "Работодатели добавлены в таблицу"
            except Exception as e:
                print(e)
                return "Ошибка в employers_to_table"


def vacancies_to_table(vacancies: List[Dict[str, dict]]) -> str | None:
    """Функция, добавляющая вакансии в таблицу"""
    create_database()
    load_dotenv()
    password = os.getenv("DATABASE_PASSWORD")
    conn_params = {
        "host": "localhost",
        "database": "vacancies",
        "user": "postgres",
        "password": password,
    }

    with psycopg2.connect(**conn_params) as conn:  # type: ignore
        with conn.cursor() as cur:
            try:
                cur.execute("DROP TABLE IF EXISTS vacancies;")
                cur.execute(
                    "CREATE TABLE vacancies (name_vacancy text not null, "
                    "employer varchar(100) not null, "
                    "location varchar(100) not null, "
                    "salary_from INT not null, salary_to INT not null, "
                    "currency varchar(10) not null, url text not null,"
                    "FOREIGN KEY (employer) REFERENCES employers(employer));"
                )
                for vacancy in vacancies:
                    name_vacancy = vacancy["name"]
                    employer = vacancy["employer"].get("name")
                    location = vacancy["area"]["name"]
                    salary_from = (
                        vacancy["salary"]["from"]
                        if vacancy["salary"]["from"] is not None
                        else 0
                    )
                    salary_to = (
                        vacancy["salary"]["to"]
                        if vacancy["salary"]["to"] is not None
                        else 0
                    )
                    currency = vacancy["salary"]["currency"]
                    url_vacancy = vacancy["alternate_url"]
                    cur.execute(
                        "INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (
                            name_vacancy,
                            employer,
                            location,
                            salary_from,
                            salary_to,
                            currency,
                            url_vacancy,
                        ),
                    )

                return "Вакансии добавлены в таблицу"
            except Exception as e:
                print(e)
                return "Ошибка в get_vacancies"


if __name__ == "__main__":
    print(employers_to_table(get_employers()))
    print(vacancies_to_table(get_vacancies(get_employers())))
