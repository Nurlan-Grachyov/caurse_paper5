from src.get_vacancies import get_vacancies, get_employers
from src.vacancies_to_table import vacancies_to_table, employers_to_table
from src.working_with_vacancies import DBManager

if __name__ == '__main__':
    print(get_vacancies(get_employers()))
    print(employers_to_table(get_employers()))
    print(vacancies_to_table(get_vacancies(get_employers())))
    obj = DBManager()
    print(obj.get_companies_and_vacancies_count())
    print(
        obj.get_all_vacancies(
            "001KZ (001КЗ)",
            "Бухгалтер по ЭСФ",
            200000,
            "https://hh.ru/vacancy/111974062",
        )
    )
    print(obj.get_all_vacancies())
    print(obj.get_avg_salary())
    print(obj.get_vacancies_with_higher_salary())
    print(obj.get_vacancies_with_keyword())