import os
from abc import ABC, abstractmethod

import psycopg2
from dotenv import load_dotenv

# from typing import Dict


class DBConnect(ABC):
    """Абстрактный метод"""

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        pass

    @abstractmethod
    def get_all_vacancies(self):
        pass

    @abstractmethod
    def get_avg_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self):
        pass


class DBManager(DBConnect):
    """Класс для работы с вакансиями из таблицы"""

    def __init__(self):
        pass

    @staticmethod
    def __connect_to_database(query: str, params: tuple | None = None) -> list:
        load_dotenv()
        password = os.getenv("DATABASE_PASSWORD")
        conn = psycopg2.connect(
            host="localhost",
            database="vacancies",
            user="postgres",
            password=password,
        )
        cur = conn.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_companies_and_vacancies_count(self):
        """Метод для получения списка всех компаний и количества вакансий у каждой компании"""
        query = """
                SELECT vacancies.employer, employers.open_vacancies FROM vacancies
                JOIN employers ON vacancies.employer = employers.employer
                GROUP BY vacancies.employer, employers.open_vacancies
                """
        results = self.__connect_to_database(query)
        for row in results:
            print(
                f"Компания: {row[0]}, Вакансия: {row[1]}, Зарплата: {row[2]}, URL: {row[3]}"
            )

    def get_all_vacancies(
        self,
        company: str | None = None,
        vacancy: str | None = None,
        salary: int | None = None,
        url: str | None = None,
    ):
        pass
        query = """
                SELECT * FROM vacancies
                WHERE (%s IS NULL OR employer ILIKE %s)
                AND (%s IS NULL OR name_vacancy ILIKE %s)
                AND (%s IS NULL OR %s BETWEEN salary_from AND salary_to)
                AND (%s IS NULL OR url = %s);
                """

        params = (
            company,
            f"%{company}%",
            vacancy,
            f"%{vacancy}%",
            salary,
            salary,
            url,
            url,
        )
        results = self.__connect_to_database(query, params)
        for row in results:
            print(
                f"Компания: {row[0]}, Вакансия: {row[1]}, Зарплата: {row[2]}, URL: {row[3]}"
            )

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass


if __name__ == "__main__":
    obj = DBManager()
    # print(obj.get_companies_and_vacancies_count())
    print(
        obj.get_all_vacancies(
            "001KZ (001КЗ)",
            "Бухгалтер по ЭСФ",
            200000,
            "https://hh.ru/vacancy/111974062",
        )
    )
