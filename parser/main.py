# This is a sample Python script.
from engine_classes import HH, SuperJob
from classes import SJVacancy, HHVacancy
from utils import sorting, get_top
from connector import Connector


def main():
    vacancy_class = None
    search_result = None
    website = None
    engine_class = None

    # Пользователь выбирает агрегатор для поиска вакансий, HeadHunter или SuperJob.
    user_choice = int(input('Для поиска через HeadHunter введи - 1.\nДля поиска через SuperJob введи - 2. \n'))
    # Устанавливаем значения переменных в соответствии с выбранным агрегатором
    if user_choice == 1:
        vacancy_class = HHVacancy
        engine_class = HH
        website = "www.hh.ru"
    elif user_choice == 2:
        vacancy_class = SJVacancy
        engine_class = SuperJob
        website = "www.superjob.ru"
    else:
        quit("Bye!")

    # Выполняем поиск вакансий по заданной должности.
    # Результат поиска записывается в атрибут класса в виде списка экземпляров.
    search_word = input('Введите должность для поиска \n')
    for i in range(1):
        if engine_class == HH:
            engine_class(search_word, i)
        else:
            search_town = input('Введите город для поиска \n')
            engine_class(search_word, i, search_town)
        if vacancy_class.get_count_of_vacancy > 0:
            print(f'По вашему запросу найдено {vacancy_class.get_count_of_vacancy} вакансий с сайта {website}:')

    is_insert = input(f'Желаете записать результат в файл {search_word.replace(" ", "_")}.json? \n')
    if is_insert.lower() == 'да':
        # По выбору пользователя записываем результат поиска в json файл с помощью класса Connector.
        # Название файла состоит из названия класса и переданного запроса.
        search_result = Connector(f'{engine_class.__name__.lower()}_{search_word.replace(" ", "_")}.json')
        dict_vac = []
        for i in vacancy_class.all_vacancies:
            x = i.get_info_vacancy()
            dict_vac.append(x)
        search_result.insert(dict_vac)

    is_print = input('Вывести результат поиска в консоль? \n')
    if is_print.lower() == 'да':
        for i in vacancy_class.all_vacancies:
            print(i)
    user_option = ""
    # Начало цикла для использования дополнительных опций с результатом поиска.
    while user_option != "стоп":
        user_option = input('\nДля дополнительных действий введите:\n'
                            '"топ" - вывод указанного количества вакансий с самыми высокими з/п\n'
                            '"удалить" - удаление из файла вакансии по названию \n'
                            '"выборка" - вывод всех вакансий по указанным параметрам \n'
                            '"стоп" - выйти из программы \n')
        # Выводим top_count вакансий по зарплате
        if user_option == 'топ':
            top_count = int(input('Сколько позиций вывести? \n'))
            top = get_top(vacancy_class.all_vacancies, top_count)
            for i in top:
                print(i)
        # Удаляем записи из файла, которые соответствуют запросу
        elif user_option == 'удалить':
            query_value = input('Введите название вакансии: \n')
            # Например - Оператор 1C
            search_result.delete({'name': query_value})
            print("Готово!")

        elif user_option == "выборка":
            user_filter = input('Введите параметр для выборки - "название" или "зарплата" ').lower()

            # Выбор данных из файла с применением фильтрации по названию.
            if user_filter == "название":
                vacancy_name = input('Введите название вакансии: \n')
                # Например - Программист 1С
                select_vacancy = search_result.select({'name': vacancy_name})
                for i in select_vacancy:
                    print(f'{i["name"]}, {i["url"]}, зарплата {i["salary"]}')

            # Выбор данных из файла с применением фильтрации по зарплате.
            if user_filter == "зарплата":
                salary_from = input('Введите нижнюю границу ')
                if salary_from == "":
                    salary_from = 0
                salary_to = input('Введите верхнюю границу ')
                if salary_to == "":
                    salary_to = 0
                if vacancy_class == HHVacancy:
                    salary_from_to = f'от {salary_from} до {salary_to} RUR'
                else:
                    salary_from_to = f'от {salary_from} до {salary_to} RUR'
                select_salary = search_result.select({"salary": salary_from_to})
                if len(select_salary) == 0:
                    print('По данному запросу вакансий не найдено')
                else:
                    for i in select_salary:
                        print(f'{i["name"]}, {i["url"]}, зарплата {i["salary"]}')


if __name__ == '__main__':
    main()
