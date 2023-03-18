from operator import itemgetter, attrgetter, methodcaller


class Vacancy:
    __slots__ = ('name', 'url_link', 'description', 'salary')

    def __init__(self, name: str, url_link: str, description: str, salary: dict) -> None:
        self.name = name
        self.url_link = url_link
        self.description = description
        self.salary = salary

    def __repr__(self) -> str:
        return f'Vacancy("{self.name}", "{self.url_link}", "{self.description}", {self.salary})'

    def __ge__(self, other: object) -> bool:
        try:
            if isinstance(other, Vacancy):
                return self.salary.get('to') >= other.salary.get('to')
        except ValueError:
            print('Не экземпляр класса Vacancy')

    def __gt__(self, other: object) -> bool:
        try:
            if isinstance(other, Vacancy):
                return self.salary.get('to') > other.salary.get('to')
        except ValueError:
            print('Не экземпляр класса Vacancy')

    def __lt__(self, other: object) -> bool:
        try:
            if isinstance(other, Vacancy):
                return self.salary.get('to') < other.salary.get('to')
        except ValueError:
            print('Не экземпляр класса Vacancy')
        except TypeError:
            print('ОШИБКА')

    def __le__(self, other: object) -> bool:
        try:
            if isinstance(other, Vacancy):
                return self.salary.get('to') <= other.salary.get('to')
        except ValueError:
            print('Не экземпляр класса Vacancy')


class CountMixin:
    """
    Считает количество экземпляров класса,
    равных количеству найденных вакансий
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    @property
    def get_count_of_vacancy(cls) -> int:
        return len(cls.all_vacancies)


class HHVacancy(CountMixin, Vacancy):  # add counter mixin
    """ HeadHunter Vacancy """
    __slots__ = tuple()

    all_vacancies = []

    def __init__(self, name: str, url_link: str, description: str, salary: dict) -> None:
        super().__init__(name, url_link, description, salary)

    def __str__(self) -> str:
        if self.salary == {'from': 0, 'to': 0, 'currency': None}:
            return f'HH: {self.name}, зарплата: не указана {self.url_link}'
        else:
            return f'HH: {self.name}, зарплата: от {self.salary.get("from")} до {self.salary.get("to")} {self.salary.get("currency")}, {self.url_link}'

    def get_info_vacancy(self) -> dict:
        info = {
            'source': 'HeadHunter',
            'name': self.name,
            'url': self.url_link,
            'description': self.description,
            'salary': f'от {self.salary.get("from")} до {self.salary.get("to")} {self.salary.get("currency")}'
        }
        return info


class SJVacancy(CountMixin, Vacancy):  # add counter mixin
    """ SuperJob Vacancy """
    __slots__ = tuple()
    all_vacancies = []

    def __init__(self, name: str, url_link: str, description: str, salary: dict) -> None:
        super().__init__(name, url_link, description, salary)

    def __str__(self) -> str:
        if self.salary == {'from': 0, 'to': 0}:
            return f'SJ: {self.name}, уровень з/п не указан {self.url_link}'
        else:
            return f'SJ: {self.name}, зарплата: от {self.salary.get("from")} до {self.salary.get("to")} руб/мес, {self.url_link}'

    def get_info_vacancy(self) -> dict:
        """
        Возвращает информацию о вакансии, которая хранится в
        экземпляре класса, в формате пригодном для записи в JSON
        """
        info = {
            'source': 'SuperJob',
            'name': self.name,
            'url': self.url_link,
            'description': self.description,
            'salary': f'от {self.salary.get("from")} до {self.salary.get("to")}'
        }
        return info
