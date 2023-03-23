from classes import SJVacancy, HHVacancy
from utils import sorting, get_top
import requests
import json
import os
from abc import ABC, abstractmethod


class Engine(ABC):
    @abstractmethod
    def get_request(self):
        pass


class HH(Engine):
    """
    Класс делает запрос к API hh.ru и создает объекты
    """

    def __init__(self, word: str, page=1) -> None:
        self.word = word
        self.page = page
        data = self.get_request()
        for i in range(20):
            try:
                self.name = data['items'][i]['name']
                self.url_link = data['items'][i]['apply_alternate_url']
                self.description = data['items'][i]['snippet']['responsibility']
                if isinstance(self.description, str):
                    self.description = self.description.replace("<highlighttext>", "").replace("</highlighttext>", "")
                try:
                    lower_threshold = data['items'][i]['salary']['from']
                    upper_threshold = data['items'][i]['salary']['to']
                    currency = data['items'][i]['salary']['currency']
                    if lower_threshold is None and upper_threshold is None:
                        self.salary = {'from': 0, 'to': 0, 'currency': None}
                    elif lower_threshold is None and upper_threshold is not None:
                        self.salary = {'from': upper_threshold, 'to': upper_threshold, 'currency': currency}
                    elif lower_threshold is not None and upper_threshold is None:
                        self.salary = {'from': lower_threshold, 'to': lower_threshold, 'currency': currency}
                    else:
                        self.salary = {'from': lower_threshold, 'to': upper_threshold, 'currency': currency}
                except TypeError:
                    self.salary = {'from': 0, 'to': 0, 'currency': None}
                HHVacancy.all_vacancies.append(HHVacancy(self.name, self.url_link, self.description, self.salary))
            except IndexError:
                print("Больше вакансий не найдено.")
                break
            except KeyError:
                print('ой')

    def get_request(self) -> dict:
        """
        Возвращает результат поиска вакансий в API HeadHunter.
        """
        response = requests.get(f'https://api.hh.ru/vacancies?text={self.word}&per_page=20&page={self.page}&area=1')
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
                try:
                    self.name = data['objects'][i]['profession']
                except NameError:
                    self.name = None
                self.url_link = data['objects'][i]['link']
                try:
                    self.description = data['objects'][i]['vacancyRichText']
                    self.description = self.description.replace("<p>", "").replace("<b>", "").replace("</b>", ""). \
                        replace("</p>", "").replace("<br />", "").replace("<ul>", "").replace("<li>", "") \
                        .replace("</li>", "").replace("</ul>", "").replace("• ", " -").replace("\n", " -"). \
                        replace("<i>", "").replace("</i>", "")
                except KeyError:
                    self.description = None
                lower_threshold = data['objects'][i]['payment_from']
                upper_threshold = data['objects'][i]['payment_to']
                if lower_threshold == 0 and upper_threshold == 0:
                    self.salary = {'from': 0, 'to': 0}
                elif lower_threshold == 0 and upper_threshold != 0:
                    self.salary = {'from': upper_threshold, 'to': upper_threshold}
                elif lower_threshold != 0 and upper_threshold == 0:
                    self.salary = {'from': lower_threshold, 'to': lower_threshold}
                else:
                    self.salary = {'from': lower_threshold, 'to': upper_threshold}
                SJVacancy.all_vacancies.append(SJVacancy(self.name, self.url_link, self.description, self.salary))
            except IndexError:
                break

    def get_request(self) -> dict:
        """
        Возвращает результат поиска вакансий в API SuperJob.
        """
        my_auth_data = {'X-Api-App-Id': os.environ['SUPERJOB_API_KEY']}
        # 'no_agreement':1 - Не показывать оклад «по договоренности» (установите параметр в 1).
        response = requests.get('https://api.superjob.ru/2.0/vacancies/',
                                headers=my_auth_data,
                                params={'keywords': {self.word}, 'page': {self.page}, 'count': 20, 'town': {self.town},
                                        'order_field': 100000, 'no_agreement': 0})
        data = response.json()
        return data
