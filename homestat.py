def make_stat(filepath):
    unusual_male_names = ('Никита', 'Илья', 'Лёва')
    unusual_female_names = ('Любовь')
    result_of_boys = {}
    result_of_girls = {}

    with open(filepath, 'r', encoding='utf-8') as file:
        last_year = 0

        for string in file:
            fullname = ''
            year = ''
            first_name_index = string.find('/>')
            second_name_index = string.find("</a>")
            if first_name_index != -1 and second_name_index != -1:
                fullname = string[first_name_index + 3:second_name_index]

            first_year_index = string.find("<h3>")
            second_year_index = string.find("</h3>")
            if first_year_index != -1 and second_year_index != -1:
                year = string[first_year_index + 4:second_year_index]

            if year != '':
                last_year = year

            if fullname != '':
                name = fullname.split()[1]
                if (name[-1] == 'а') or (name[-1] == 'я') or (
                        name in unusual_female_names):
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

                else:
                    if last_year in result_of_boys.keys():
                        if name in result_of_boys[last_year].keys():
                            result_of_boys[last_year][name] += 1
                        else:
                            result_of_boys[last_year][name] = 1
                    else:
                        result_of_boys[last_year] = {name: 1}
        return {'girls_stat': result_of_girls, 'boys_stat': result_of_boys}


def extract_years(stat):
    return sorted(
        list(stat['girls_stat'].keys()) or list(stat['boys_stat'].keys()))


def extract_general_indefinite(stat, sex):
    answer_list = []
    general_stat = {}

    sex_dict = stat['girls_stat' if sex == 'girls' else 'boys_stat']

    for key in extract_years(stat):
        for i in sex_dict[key].keys():
            if i in general_stat.keys():
                general_stat[i] += sex_dict[key][i]
            else:
                general_stat[i] = sex_dict[key][i]

    for key in general_stat:
        answer_list.append((key, general_stat[key]))

    return sorted(answer_list, key=lambda x: x[1], reverse=True)


def extract_general_male(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён мальчиков.
    Список должен быть отсортирован по убыванию количества.
    """
    return extract_general_indefinite(stat, 'boys')


def extract_general_female(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён девочек.
    Список должен быть отсортирован по убыванию количества.
    """
    return extract_general_indefinite(stat, 'girls')


def extract_general(stat):
    return sorted(extract_general_male(stat) + extract_general_female(stat),
                  key=lambda x: x[1],
                  reverse=True)


def extract_year_indefinite(stat, year, sex):
    answer_list = []
    general_stat = {}
    sex_dict = stat['girls_stat' if sex == 'girls' else 'boys_stat']
    key = year

    for i in sex_dict[key].keys():
        if i in general_stat.keys():
            general_stat[i] += sex_dict[key][i]
        else:
            general_stat[i] = sex_dict[key][i]

    for key in general_stat.keys():
        answer_list.append((key, general_stat[key]))

    return sorted(answer_list, key=lambda x: x[1], reverse=True)


def extract_year_male(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён мальчиков в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    return extract_year_indefinite(stat, year, 'boys')


def extract_year_female(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён девочек в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    return extract_year_indefinite(stat, year, 'girls')


def extract_year(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    return sorted(
        extract_year_male(stat, year) + extract_year_female(stat, year),
        key=lambda x: x[1],
        reverse=True)
