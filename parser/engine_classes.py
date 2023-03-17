from classes import SJVacancy, HHVacancy
import requests
import json
import os

from abc import ABC, abstractmethod
from pprint import pprint


class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass

    @staticmethod
    def get_connector(file_name):
        """ Возвращает экземпляр класса Connector """
        pass


class HH(Engine):
    """Метод делает запрос к API hh.ru и создает объекты"""

    def __init__(self, word: str, page=1, town='Moscow'):
        self.word = word
        self.page = page
        # ГОРОД НЕ ИСПОЛЬЗУЕТСЯ
        self.town = town
        data = self.get_request()
        # pprint(data)
        for i in range(10):
            try:
                self.name = data['items'][i]['name']
                self.url_link = data['items'][i]['apply_alternate_url']
                self.description = data['items'][i]['snippet']['responsibility']
                try:
                    self.salary = {'from': data['items'][i]['salary']['from'], 'to': data['items'][i]['salary']['to']}
                except TypeError:
                    self.salary = {}
                HHVacancy.all_vacancies.append(HHVacancy(self.name, self.url_link, self.description, self.salary))
            except IndexError:
                print("Больше вакансий не найдено.")
                break

    def get_request(self):
        # Разобраться как изменить город
        response = requests.get(f'https://api.hh.ru/vacancies?text={self.word}&per_page=10&page={self.page}&area=1')
        data = response.json()
        return data


class SuperJob(Engine):
    def __init__(self, word: str, page=1, town='Moscow'):

        self.word = word
        self.page = page
        self.town = town
        data = self.get_request()
        for i in range(20):
            try:
                # pprint(data)
                try:
                    self.name = data['objects'][i]['profession']
                except NameError:
                    self.name = None
                self.url_link = data['objects'][i]['link']
                try:
                    self.description = data['objects'][i]['client']['description']
                except TypeError:
                    self.description = None
                self.salary = {'from': data['objects'][i]['payment_from'], 'to': data['objects'][i]['payment_to']}
                SJVacancy.all_vacancies.append(SJVacancy(self.name, self.url_link, self.description, self.salary))
            except IndexError:
                print("Больше вакансий не найдено.")
                break

    def get_request(self):
        # https://api.superjob.ru/#gettin прочитать про order_field
        # 'no_agreement':1 - Не показывать оклад «по договоренности» (установите параметр в 1).
        my_auth_data = {'X-Api-App-Id': os.environ['SUPERJOB_API_KEY']}
        response = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                headers=my_auth_data,
                                params={'keywords': {self.word}, 'page': {self.page}, 'count': 20, 'town': {self.town},
                                        'order_field': 100000, 'no_agreement': 0})
        data = response.json()
        return data


for i in range(1):
    hh = HH('python', i)

for i in HHVacancy.all_vacancies:
    print(i)
print(HHVacancy.get_count_of_vacancy)

# for i in range(1):
#     sj = SuperJob("python", i, 'Москва')
#
# for i in SJVacancy.all_vacancies:
#        print(i)
#
# print(SJVacancy.get_count_of_vacancy)
