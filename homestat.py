import re
import urllib.request


def make_stat(url):
    unusual_male_names = ('Никита', 'Илья', 'Лёва')
    unusual_female_names = ('Любовь')
    result_of_boys = {}
    result_of_girls = {}

    try:
        get_url = urllib.request.urlopen(url)
        last_year = 0

        for string in get_url:
            decoded_string = string.decode('windows-1251')
            year = re.findall(r'(?<=<h3>)(.*)(?=</h3>)', decoded_string)
            fullname = re.findall(r'(?<=/>)(.*)(?=</a>)', decoded_string)

            if len(year) != 0:
                last_year = int(year[0])

            if len(fullname) != 0:
                name = fullname[0].split()[1]
                if name[-1] == 'а' or name[-1] == 'я':
                    if name in unusual_male_names:
                        if last_year in result_of_boys.keys():
                            if name in result_of_boys[last_year].keys():
                                result_of_boys[last_year][name] += 1
                            else:
                                result_of_boys[last_year][name] = 1
                        else:
                            result_of_boys[last_year] = {name: 1}

                    else:
                        if last_year in result_of_girls.keys():
                            if name in result_of_girls[last_year].keys():
                                result_of_girls[last_year][name] += 1
                            else:
                                result_of_girls[last_year][name] = 1
                        else:
                            result_of_girls[last_year] = {name: 1}

                elif name in unusual_female_names:
                    if last_year in result_of_girls.keys():
                        if name in result_of_girls[last_year].keys():
                            result_of_girls[last_year][name] += 1
                        else:
                            result_of_girls[last_year][name] = 1
                    else:
                        result_of_girls[last_year] = {name: 1}

                else:
                    if last_year in result_of_boys.keys():
                        if name in result_of_boys[last_year].keys():
                            result_of_boys[last_year][name] += 1
                        else:
                            result_of_boys[last_year][name] = 1
                    else:
                        result_of_boys[last_year] = {name: 1}
        return {"Code": 0, "Answer": {'girls_stat': result_of_girls,
                                      'boys_stat': result_of_boys}}
    except urllib.error.URLError:
        return {"Code": 1, "Answer": ""}

    """
    Функция вычисляет статистику по именам за каждый год с учётом пола.
    """


def extract_years(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список годов,
    упорядоченный по возрастанию.
    """
    return sorted(
        list(stat['Answer']['girls_stat'].keys()) or
        list(stat['Answer']['boys_stat'].keys()))


# print(make_stat('http://shannon.usu.edu.ru/ftp/python/hw2/home.html')['Answer']['girls_stat'])
# print(extract_years(make_stat('http://shannon.usu.edu.ru/ftp/python/hw2/home.html')))

def extract_general(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для всех имён.
    Список должен быть отсортирован по убыванию количества.
    """
    answer_list = []

    girls_dict = stat['Answer']['girls_stat']
    boys_dict = stat['Answer']['boys_stat']
    for key in extract_years(stat):
        for i in girls_dict[key].keys():
            answer_list.append((i, girls_dict[key][i]))
        for i in boys_dict[key].keys():
            answer_list.append((i, boys_dict[key][i]))
    return sorted(answer_list, key=lambda x: x[1], reverse=True)


stat = make_stat('http://shannon.usu.edu.ru/ftp/python/hw2/home.html')
print(extract_general(stat))


def extract_general_male(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён мальчиков.
    Список должен быть отсортирован по убыванию количества.
    """
    answer_list = []

    boys_dict = stat['Answer']['boys_stat']
    for key in extract_years(stat):

        for i in boys_dict[key].keys():
            answer_list.append((i, boys_dict[key][i]))
    return sorted(answer_list, key=lambda x: x[1], reverse=False)


def extract_general_female(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён девочек.
    Список должен быть отсортирован по убыванию количества.
    """
    answer_list = []

    girls_dict = stat['Answer']['girls_stat']
    for key in extract_years(stat):

        for i in girls_dict[key].keys():
            answer_list.append((i, girls_dict[key][i]))
    return sorted(answer_list, key=lambda x: x[1], reverse=False)


def extract_year(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    answer_list = []

    girls_dict = stat['Answer']['girls_stat']
    boys_dict = stat['Answer']['boys_stat']

    for i in girls_dict[year].keys():
        answer_list.append((i, girls_dict[year][i]))
    for i in boys_dict[year].keys():
        answer_list.append((i, boys_dict[year][i]))
    return sorted(answer_list, key=lambda x: x[1], reverse=False)


def extract_year_male(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён мальчиков в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    answer_list = []

    boys_dict = stat['Answer']['boys_stat']
    for i in boys_dict[year].keys():
        answer_list.append((i, boys_dict[year][i]))
    return sorted(answer_list, key=lambda x: x[1], reverse=False)


def extract_year_female(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён девочек в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    answer_list = []

    girls_dict = stat['Answer']['girls_stat']
    for i in girls_dict[year].keys():
        answer_list.append((i, girls_dict[year][i]))
    return sorted(answer_list, key=lambda x: x[1], reverse=False)


if __name__ == '__main__':
    pass
