import csv
import sys
from datetime import datetime
import var_dump as vd

from prettytable import PrettyTable
from var_dump import var_dump

file = input('Введите название файла: ')


def сsv_reader(ﬁle_name):
    with open(ﬁle_name, "r", encoding='utf_8') as file:
        readerFile = csv.reader(file, delimiter=",")
        data = list(readerFile)
        try:
            title = data[0]
        except:
            title = []
        result = [x for x in data[1:] if len(x) == len(title) and x.count('') == 0]
        return result, title


def csv_ﬁler(reader):
    dataV = []
    dataVacancy = []
    dataVacancy_append = dataVacancy.append
    dict = {}
    read = reader[0]
    return method_name(dataV, dataVacancy, dataVacancy_append, dict, read, reader)


def method_name(dataV, dataVacancy, dataVacancy_append, dict, read, reader):
    for vacancy in read:
        for keys, val in enumerate(vacancy):
            import re
            temp = re.sub('<[^<]+?>', '', val)
            if reader[1][keys] != 'key_skills':
                temp = ', '.join(temp.split('\n'))
            temp = ' '.join(temp.split())
            if reader[1][keys] == 'key_skills':
                dict[reader[1][keys]] = val
            else:
                dict[reader[1][keys]] = temp
        for key in dict.keys():
            dataV.append(dict[key])
        dataVacancy_append(dataV)
        dataV = []
    return dataVacancy


def formatter(row, translation_exp, translation_bool, translation_money):
    new_skills = row[2].split('\n')
    row[2] = '\n'.join(new_skills)
    row[3] = translate(row[3], translation_exp)
    row[4] = translate(row[4], translation_bool)
    row[9] = translate(row[9], translation_money)
    return row


def filterR(row, column_name, column_data, spisok2) -> bool:
    isRight = False
    if column_name == []:
        return isRight

    def premiym_filterR(row, column_name, column_data, spisok2, isRight):
        isRight = True if column_data == row[4] else False
        return isRight

    def name_filterR(row, column_name, column_data, spisok2, isRight):
        for index, val in enumerate(spisok2):
            if column_name == val:
                if row[index] == column_data:
                    isRight = True
        return isRight

    def money_filterR(row, column_name, column_data, spisok2, isRight):
        isRight = True if int(float(row[7])) >= int(column_data) >= int(float(row[6])) else False
        return isRight

    def time_filterR(row, column_name, column_data, spisok2, isRight):
        temp = f'{row[11][8]}{row[11][9]}.{row[11][5]}{row[11][6]}.{row[11][0]}{row[11][1]}{row[11][2]}{row[11][3]}'
        isRight = True if temp == column_data else False
        return isRight

    def skill_filterR(row, column_name, column_data, spisok2, isRight):
        countSkill = 0
        filterRSkills = column_data.split(', ')
        filterRSkillsRow = row[2].split('\n')
        for i in filterRSkills:
            for j in filterRSkillsRow:
                if j.strip().replace('...', '') == i.strip():
                    countSkill += 1
        if len(filterRSkills) == countSkill:
            isRight = True
        return isRight

    def exp_filterR(row, column_name, column_data, spisok2, isRight):
        if row[3] == column_data:
            isRight = True
        return isRight

    def valuta_filterR(row, column_name, column_data, spisok2, isRight):
        if row[9] == column_data:
            isRight = True
        return isRight

    def area_filterR(row, column_name, column_data, spisok2, isRight):
        isRight = True if row[10] == column_data else False
        return isRight

    filterR_title = {
        'Название': name_filterR,
        'Описание': name_filterR,
        'Навыки': skill_filterR,
        'Опыт работы': exp_filterR,
        'Премиум-вакансия': premiym_filterR,
        'Компания': name_filterR,
        'Оклад': money_filterR,
        'Название региона': area_filterR,
        'Дата публикации вакансии': time_filterR,
        'Идентификатор валюты оклада': valuta_filterR,
    }

    return filterR_title[column_name](row, column_name, column_data, spisok2, isRight)


def addingNumber(table, listRows):
    listRows = is_len_correct(listRows)
    table.add_rows(listRows)
    table._field_names.insert(0, '№')
    table._align['№'] = 'c'
    table._valign['№'] = 't'
    for i, _ in enumerate(table._rows):
        table._rows[i].insert(0, i + 1)
    return table


def tableToString(listRows, table, page, headings):
    table = addingNumber(table, listRows)
    tableGetString = table.get_string(start=int(page[0]) - 1, end=int(page[1]) - 1, fields=headings)
    return tableGetString


def csv_sorted(table, page, headings, isReversed, parametrSorted, dic_naming, listRows):
    def name_function(table, page, headings, isReversed, parametrSorted, dic_naming, listRows):
        listRows.sort(key=lambda x: x[dic_naming.index(parametrSorted)], reverse=isReversed)
        return tableToString(listRows, table, page, headings)

    def exp_function(table, page, headings, isReversed, parametrSorted, dic_naming, listRows):
        listRows.sort(key=lambda x: experiance(x[3]), reverse=not isReversed)
        return tableToString(listRows, table, page, headings)

    def skills_function(table, page, headings, isReversed, parametrSorted, dic_naming, listRows):
        listRows.sort(key=lambda x: x[2].count('\n'), reverse=isReversed)
        return tableToString(listRows, table, page, headings)

    def money_function(table, page, headings, isReversed, parametrSorted, dic_naming, listRows):
        listRows.sort(key=lambda x: oklad(float(x[6]),float(x[7]),x[9]), reverse=isReversed)
        return tableToString(listRows, table, page, headings)

    def time_function(table, page, headings, isReversed, parametrSorted, dic_naming, listRows):
        listRows.sort(key=lambda x: data(x[11]), reverse=isReversed)
        return tableToString(listRows, table, page, headings)

    sort_title = {
        'Название': name_function,
        'Описание': name_function,
        'Навыки': skills_function,
        'Опыт работы': exp_function,
        'Премиум-вакансия': name_function,
        'Компания': name_function,
        'Оклад': money_function,
        'Название региона': name_function,
        'Дата публикации вакансии': time_function,

    }

    return sort_title[parametrSorted](table, page, headings, isReversed, parametrSorted, dic_naming, listRows)


def experiance(string) -> int:
    dict = {"Нет опыта": 3, "От 1 года до 3 лет": 2, "От 3 до 6 лет": 1, "Более 6 лет": 0}
    return dict[string]


def data(string):
    stringsplit = string.split('T')
    data_stringsplit = stringsplit[0].split('-')
    time_stringsplit = stringsplit[1].split(':')
    datalist = [int(data_stringsplit[0]), int(data_stringsplit[1]), int(data_stringsplit[2]),
                int(time_stringsplit[0]), int(time_stringsplit[1]), int(time_stringsplit[2][:2])]
    return datalist


def oklad(number1,number2,valuta) -> float:
    if valuta != 'Рубли':
        if valuta == 'Манаты':
            number1 *= 35.68
            number2 *= 35.68
        elif valuta == 'Белорусские рубли':
            number1 *= 23.91
            number2 *= 23.91
        elif valuta == 'Евро':
            number1 *= 59.90
            number2 *= 59.90
        elif valuta == 'Грузинский лари':
            number1 *= 21.74
            number2 *= 21.74
        elif valuta == 'Киргизский сом':
            number1 *= 0.76
            number2 *= 0.76
        elif valuta == 'Тенге':
            number1 *= 0.13
            number2 *= 0.13
        elif valuta == 'Гривны':
            number1 *= 1.64
            number2 *= 1.64
        elif valuta == 'Доллары':
            number1 *= 60.66
            number2 *= 60.66
        elif valuta == 'Узбекский сум':
            number1 *= 0.0055
            number2 *= 0.0055
    return (number1 + number2) / 2


def is_len_correct(dic_data):
    for index1, list in enumerate(dic_data):
        for index2, word in enumerate(list):
            if len(dic_data[index1][index2]) > 100 and index2 == 2:
                dic_data[index1][index2] = word[:100] + '...'
                if word[len(word) - 4] == '\n':
                    dic_data[index1][index2] = word[:len(word) - 4] + '...'
            elif len(word) > 100:
                dic_data[index1][index2] = word[:100] + '...'
            if index2 == 11:
                dic_data[index1][index2] = datetime.strptime(dic_data[index1][index2], '%Y-%m-%dT%H:%M:%S%z').strftime(
                    '%d.%m.%Y')
        if list[8] == 'False':
            list[8] = 'С вычетом налогов'
        elif list[8] == 'True':
            list[8] = 'Без вычета налогов'
        num1 = str(int(float(list[6])))
        num2 = str(int(float(list[7])))
        if len(num1) >= 4:
            num1F = num1[:len(num1) - 3] + ' ' + num1[-3:]
        else:
            num1F = num1[-3:]
        if len(num2) >= 4:
            num2F = num2[:len(num2) - 3] + ' ' + num2[-3:]
        else:
            num2F = num2[-3:]
        list[6] = f'{num1F} - {num2F} ({list[9]}) ({list[8]})'
        list.remove(list[7])
        list.remove(list[7])
        list.remove(list[7])
    return dic_data


def translate(string, translate):
    new_list = []
    for i in string.split():
        if i in translate.keys():
            i = translate.get(i)
        else:
            i = i
        new_list.append(i)

    return " ".join(new_list)


def print_vacancies(data_vacancies, dic_naming, dic_naming2, translations_title, translation_money, translations_bool,
                    translations_exp, parametrfilterR, parametrSort, isReversSort, pageInput, headings):
    exitMessage = ''
    column_name = []
    column_data = []
    isCorrectData = True
    if parametrfilterR.find(': ') != -1 and len(parametrfilterR) != 0:
        parametrfilterR_split = parametrfilterR.split(': ')
        column_name = parametrfilterR_split[0]
        column_data = parametrfilterR_split[1]
    elif parametrfilterR.find(': ') == -1 and len(parametrfilterR) != 0:
        exitMessage = 'Формат ввода некорректен'
        isCorrectData = False
    if parametrfilterR.find(': ') != -1 and column_name not in dic_naming2:
        exitMessage = 'Параметр поиска некорректен '
        isCorrectData = False
    for name in dic_naming2:
        if column_name == name:
            break

    if parametrSort not in dic_naming and parametrSort != '':
        exitMessage = 'Параметр сортировки некорректен'
        isCorrectData = False

    if isReversSort == 'Да':
        isReversSortTranslate = True
    elif isReversSort == 'Нет':
        isReversSortTranslate = False
    elif isReversSort == '':
        isReversSortTranslate = False
    else:
        exitMessage = 'Порядок сортировки задан некорректно'
        isCorrectData = False

    page = [1, len(data_vacancies) + 1]
    if pageInput != '':
        pageI = pageInput.split(' ')
        for index, val in enumerate(pageI):
            page[index] = val

    if headings == ['']:
        headings = ''
    else:
        headings.insert(0, '№')
    newTable = PrettyTable(['Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия', 'Компания',
                            'Оклад', 'Название региона', 'Дата публикации вакансии'])
    list_rows = []
    newTable.hrules = True
    newTable.max_width = 20
    newTable.align = 'l'

    if isCorrectData:
        formatter_vacancy = list(
            map(lambda x: formatter(x, translations_exp, translations_bool, translation_money), data_vacancies))
        count = len(formatter_vacancy)+1
        list_rows = formatter_vacancy
        if column_data:
            vacancy_filterR = list(filter(lambda x: filterR(x, column_name, column_data, spisok3),
                                          formatter_vacancy))
            count = len(vacancy_filterR)+1
            list_rows = vacancy_filterR
        if not сsv_reader(file)[1]:
            print("Пустой файл")
            sys.exit()
        elif not сsv_reader(file)[0]:
            print("Нет данных")
            sys.exit()
        if count == 1 or int(page[0]) >= count :
            print('Ничего не найдено')
        else:
            if parametrSort == '':
                addingNumber(newTable, list_rows)
                table = (newTable.get_string(start=int(page[0]) - 1, end=int(page[1]) - 1, fields=headings))
                print(table)
            else:
                table = csv_sorted(newTable, page, headings, isReversSortTranslate, parametrSort, dic_naming2, list_rows)
                print(table)
    else:
        print(exitMessage)
        sys.exit()


translations_title = {
    'name': 'Название',
    'description': 'Описание',
    'key_skills': 'Навыки',
    'experience_id': 'Опыт работы',
    'premium': 'Премиум-вакансия',
    'employer_name': 'Компания',
    'salary_from': 'Нижняя граница вилки оклада',
    'salary_to': 'Верхняя граница вилки оклада',
    'salary_gross': 'Оклад указан до вычета налогов',
    'salary_currency': 'Идентификатор валюты оклада',
    'area_name': 'Название региона',
    'published_at': 'Дата публикации вакансии',
}
translations_bool = {
    'True': 'Да',
    'False': 'Нет',
}
translations_money = {
    'AZN': 'Манаты',
    'BYR': 'Белорусские рубли',
    'EUR': 'Евро',
    'GEL': 'Грузинский лари',
    'KGS': 'Киргизский сом',
    'KZT': 'Тенге',
    'RUR': 'Рубли',
    'UAH': 'Гривны',
    'USD': 'Доллары',
    'UZS': 'Узбекский сум',
}
translations_exp = {
    'noExperience': 'Нет опыта',
    'between1And3': 'От 1 года до 3 лет',
    'between3And6': 'От 3 до 6 лет',
    'moreThan6': 'Более 6 лет'
}

spisok2 = ['Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия', 'Компания',
           'Оклад', 'Название региона', 'Дата публикации вакансии']
spisok3 = ['Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия', 'Компания',
           'Нижняя граница вилки оклада', 'Верхняя граница вилки оклада', 'Оклад',
           'Идентификатор валюты оклада', 'Название региона', 'Дата публикации вакансии']

parametrfilterR = input('Введите параметр фильтрации: ')

parametrSort = input('Введите параметр сортировки: ')

isReversSort = input('Обратный порядок сортировки (Да / Нет): ')

pageInput = input('Введите диапазон вывода: ')

headings = input('Введите требуемые столбцы: ').split(', ')

print_vacancies(csv_ﬁler(сsv_reader(file)), spisok2, spisok3, translations_title, translations_money, translations_bool,
                translations_exp, parametrfilterR, parametrSort, isReversSort, pageInput, headings)
