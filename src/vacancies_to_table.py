from typing import List

import psycopg2

from src.get_vacancies import get_vacancies


def vacancies_to_table(vacancies: List) -> str:
    """Функция, добавляющая вакансии в таблицу"""
    conn_params = {
        "host": "localhost",
        "database": "vacancies",
        "user": "postgres",
        "password": "07052001",
    }

    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("DROP TABLE IF EXISTS vacancies;")
                cur.execute(
                    "CREATE TABLE vacancies (name_vacancy text not null, "
                    "location varchar(100) not null, "
                    "salary_from INT not null, salary_to INT not null, "
                    "currency varchar(10) not null, url text not null);"
                )
                for vacancy in vacancies:
                    name_vacancy = vacancy["name"]
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
                    if True:
                        cur.execute(
                            "INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s)",
                            (
                                name_vacancy,
                                location,
                                salary_from,
                                salary_to,
                                currency,
                                url_vacancy,
                            ),
                        )
                        conn.commit()
                return "Вакансии добавлены в таблицу"
            except Exception as e:
                print(e)
                return "Ошибка в get_vacancies"


if __name__ == "__main__":
    print(vacancies_to_table(get_vacancies()))
