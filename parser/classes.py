from operator import itemgetter, attrgetter, methodcaller



class Vacancy:
    # __slots__ = ...

    def __init__(self, name, url_link, description, salary):
        self.name = name
        self.url_link = url_link
        self.description = description
        self.salary = salary

    def __str__(self):
        pass

    def __repr__(self):
        return f'Vacancy("{self.name}", "{self.url_link}", "{self.description}", {self.salary})'

    def __ge__(self, other):
        try:
            if isinstance(other, Vacancy):
                return self.salary.get('to') >= other.salary.get('to')
        except ValueError:
            print('Не экземпляр класса Vacancy')

    def __gt__(self, other):
        try:
            if isinstance(other, Vacancy):
                return self.salary.get('to') > other.salary.get('to')
        except ValueError:
            print('Не экземпляр класса Vacancy')

    def __lt__(self, other):
        try:
            if isinstance(other, Vacancy):
                return self.salary.get('to') < other.salary.get('to')
        except ValueError:
            print('Не экземпляр класса Vacancy')
        except TypeError:
            print('ОШИБКА')

    def __le__(self, other):
        try:
            if isinstance(other, Vacancy):
                return self.salary.get('to') <= other.salary.get('to')
        except ValueError:
            print('Не экземпляр класса Vacancy')

class CountMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    @property
    def get_count_of_vacancy(cls):
        return len(cls.all_vacancies)


class HHVacancy(CountMixin, Vacancy):  # add counter mixin
    """ HeadHunter Vacancy """
    all_vacancies = []

    def __init__(self, name, url_link, description, salary):
        super().__init__(name, url_link, description, salary)

    def __str__(self):
        if self.salary == {'from': 0, 'to': 0, 'currency': None}:
            return f'HH: {self.name}, зарплата: не указана {self.url_link}'
        else:
            return f'HH: {self.name}, зарплата: от {self.salary.get("from")} до {self.salary.get("to")} {self.salary.get("currency")} {self.url_link}'


class SJVacancy(CountMixin, Vacancy):  # add counter mixin
    """ SuperJob Vacancy """
    all_vacancies = []

    def __init__(self, name, url_link, description, salary):
        super().__init__(name, url_link, description, salary)

    def __str__(self):
        if self.salary == {'from': 0, 'to': 0}:
            return f'SJ: {self.name}, уровень з/п не указан {self.url_link}'
        else:
            return f'SJ: {self.name}, зарплата: от {self.salary.get("from")} до {self.salary.get("to")} руб/мес {self.url_link}'


def sorting(vacancies: list, level="from"):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    sort_list_vacancy = sorted(vacancies, key=lambda vacancy: vacancy.salary.get(level))
    # sort_list_vacancy = sorted(vacancies)
    return sort_list_vacancy


def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    top_vacancies = sorting(vacancies)[-top_count:]
    return top_vacancies
