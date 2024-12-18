import requests


def get_vacancies():
    url_1 = "https://api.hh.ru/employers"
    params = {"only_with_vacancies": True}
    try:
        employer_json = requests.get(url_1, params=params)
        if employer_json.status_code == 200:
            employers = employer_json.json().get("items")[:10]
            # return employers
            all_vacancies = []
            if employers:
                for employer in employers:
                    employer_id = employer.get("id")
                    params_1 = {"employer_id": employer_id}
                    url = "https://api.hh.ru/vacancies"
                    vacancies_json = requests.get(url, params=params_1)
                    vacancies = vacancies_json.json().get("items")
                    for vacancy in vacancies:
                        if (
                            vacancy.get("name") is not None
                            and vacancy["area"].get("name") is not None
                            and vacancy.get("salary") is not None
                            and vacancy["salary"].get("currency") is not None
                            and vacancy.get("alternate_url") is not None
                        ):
                            all_vacancies.append(vacancy)
            return all_vacancies
    except Exception as e:
        print(e)
        print("Ошибка в get_vacancies")
        return []


if __name__ == "__main__":
    print(get_vacancies())