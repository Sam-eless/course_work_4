import requests
import json
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

    def __init__(self):
        data = self.get_request()
        pprint(data)
        self.name = data['items'][0]['name']
        self.url_link = data['items'][0]['apply_alternate_url']
        self.description = data['items'][0]['snippet']['responsibility']
        self.money = data['items'][0]['salary']['from'], data['items'][0]['salary']['to']
        self.currency = data['items'][0]['salary']['to']

    def get_request(self):
        response = requests.get('https://api.hh.ru/vacancies?text=Python&per_page=1&page=0')
        data = response.json()
        return data


class SuperJob(Engine):
    def get_request(self):
        pass


hh = HH()
