def sorting(vacancies: list, level="from"):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    sort_list_vacancy = sorted(vacancies, key=lambda vacancy: vacancy.salary.get(level))
    # sort_list_vacancy = sorted(vacancies)
    return sort_list_vacancy


def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    top_vacancies = sorting(vacancies)[-top_count:]
    return top_vacancies
