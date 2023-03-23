import os
import time
import json


class Connector:
    """
    Класс коннектор к файлу
    """

    def __init__(self, data_file: str) -> None:
        self.__data_file = self.data_file = data_file

    @property
    def data_file(self) -> str:
        return self.__data_file

    @data_file.setter
    def data_file(self, value: str) -> None:
        if self.__connect():
            self.__data_file = value
        else:
            raise ValueError("Файл не найден")

    def __connect(self) -> bool:
        """
        Проверка на существование файла с данными и создание его при необходимости.
        Проверка актуальности файла, если создан больше суток назад - вызывается исключение.
        """
        if not os.path.exists(self.__data_file):
            my_file = open(self.__data_file, "w")
            my_file.close()
            return True
        elif (os.path.getmtime(self.__data_file) - time.time()) * -1 > 86400:
            raise Exception("Файл изменялся более суток назад")
        else:
            return True

    def insert(self, data: list) -> None:
        """
        Запись данных в файл с сохранением структуры и исходных данных.
        """
        data = json.dumps(data, indent=4, ensure_ascii=False)
        with open(self.__data_file, "w", encoding="UTF-8") as file:
            file.write(data)

    def select(self, query: dict) -> list:
        """
        Выбор данных из файла с применением фильтрации.
        Query содержит словарь в котором ключ это поле для фильтрации,
        а значение это искомое значение.
        Например: {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000.
        """
        with open(self.__data_file, "r", encoding="UTF-8") as file:
            data = json.load(file)
            sorted_data = []
            try:
                for i in data:
                    # if isinstance(i[key], str):
                    for key in query.keys():
                        if query[key] in i[key]:
                            sorted_data.append(i)
            except KeyError:
                print("Нет данных по указанному ключу")
            return sorted_data

    def delete(self, query: dict) -> None:
        """
        Удаление записей из файла, которые соответствуют запросу.
        Если в query передан пустой словарь, то функция удаления не сработает
        """
        with open(self.__data_file, "r", encoding="UTF-8") as file:
            data = json.load(file)
            sorted_data = []
            for i in data:
                if query == {}:
                    print('Не переданы данные для удаления')
                    break
                else:
                    for key in query.keys():
                        if i[key] != query[key]:
                            sorted_data.append(i)
                with open(self.__data_file, 'w', encoding='utf8') as outfile:
                    json.dump(sorted_data, outfile, ensure_ascii=False, indent=2)
