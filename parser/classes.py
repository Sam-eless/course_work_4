# from parser.engine_classes import SuperJob


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
        return f'Vacancy({self.name}, {self.url_link}, {self.description}, {self.salary}'


class CountMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    @property
    def get_count_of_vacancy(self):
        return len(self.all_vacancies)


class HHVacancy(CountMixin, Vacancy):  # add counter mixin
    """ HeadHunter Vacancy """
    all_vacancies = []

    def __init__(self, name, url_link, description, salary):
        super().__init__(name, url_link, description, salary)

    def __str__(self):
        return f'SJ: {self.name}, зарплата: {self.salary} руб/мес {self.url_link}'


class SJVacancy(CountMixin, Vacancy):  # add counter mixin
    """ SuperJob Vacancy """
    all_vacancies = []

    def __init__(self, name, url_link, description, salary):
        super().__init__(name, url_link, description, salary)

    def __str__(self):
        return f'SJ: {self.name}, зарплата: {self.salary} руб/мес {self.url_link}'


def sorting(vacancies):
    """ Должен сортировать любой список вакансий по ежемесячной оплате (gt, lt magic methods) """
    pass


def get_top(vacancies, top_count):
    """ Должен возвращать {top_count} записей из вакансий по зарплате (iter, next magic methods) """
    pass
#
# sj = SuperJob("python")
# print(SJVacancy.all_vacancies)
