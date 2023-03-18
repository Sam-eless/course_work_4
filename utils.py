def sorting(vacancies: list, level="from") -> list:
    """
    Сортирует список вакансий по ежемесячной оплате.
    """
    sort_list_vacancy = sorted(vacancies, key=lambda vacancy: vacancy.salary.get(level))
    # sort_list_vacancy = sorted(vacancies)
    return sort_list_vacancy


def get_top(vacancies: list, top_count: int) -> list:
    """
    Возвращает {top_count} записей из вакансий по зарплате.
    """
    top_vacancies = sorting(vacancies)[-top_count:]
    return top_vacancies
