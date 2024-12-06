import os
from abc import ABC, abstractmethod

import psycopg2
from dotenv import load_dotenv


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
    def connect_to_database(query: str, params: tuple | None = None) -> list:
        """Подключаемся к базе данных"""
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
        results = self.connect_to_database(query)
        return results


    def get_all_vacancies(
        self,
        company: str | None = None,
        vacancy: str | None = None,
        salary: int | None = None,
        url: str | None = None,
    ):
        """Метод для получения списка всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию."""
        query = """
                SELECT * FROM vacancies
                WHERE (%s IS NULL OR employer ILIKE %s)
                AND (%s IS NULL OR name_vacancy ILIKE %s)
                AND (%s IS NULL OR 
               (salary_to = 0 AND %s >= salary_from) OR 
               (salary_from IS NOT NULL AND salary_to IS NOT NULL AND %s BETWEEN salary_from AND salary_to))
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
        results = self.connect_to_database(query, params)
        vacancies = []
        for row in results:
            vacancies.append(
                {
                    "Компания": row[1],
                    "Вакансия": row[0],
                    "Зарплата": row[3],
                    "URL": row[6],
                }
            )
        return vacancies

    def get_avg_salary(self):
        """Метод, получающий среднюю зарплату по вакансиям."""
        query = "SELECT round(AVG(salary_from), 2) AS avg_salary FROM vacancies"
        results = self.connect_to_database(query)
        avg_salary = results[0][0] if results and results[0] else None
        return avg_salary

    def get_vacancies_with_higher_salary(self):
        """Метод, получающий список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        query = """SELECT * FROM vacancies
        WHERE (salary_from + salary_to) / 2 > (SELECT round(AVG((salary_from + salary_to) / 2), 2)
        AS AVG_SALARY FROM vacancies)"""
        results = self.connect_to_database(query)
        vacancies = []
        for row in results:
            vacancies.append(
                {
                    "Компания": row[1],
                    "Вакансия": row[0],
                    "Зарплата": row[3],
                    "URL": row[6],
                }
            )
        return vacancies

    def get_vacancies_with_keyword(self):
        """Метод, получающий список всех вакансий,
         в названии которых содержатся переданные в метод слова, например python."""
        query = "SELECT * FROM vacancies WHERE name_vacancy ILIKE '%менеджер%'"
        results = self.connect_to_database(query)

        return results


if __name__ == "__main__":
    obj = DBManager()
    # print(obj.get_companies_and_vacancies_count())
    print(
        obj.get_all_vacancies(
            "0250",
            "Менеджер по продажам",
            60000,
            # "https://hh.ru/vacancy/112147530",
        )
    )
    # print(obj.get_all_vacancies())
    # print(obj.get_avg_salary())
    # print(obj.get_vacancies_with_higher_salary())
    # print(obj.get_vacancies_with_keyword())
    # print(obj.connect_to_database("SELECT * FROM vacancies"))