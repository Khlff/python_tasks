def make_stat(filepath):
    unusual_male_names = ('Никита', 'Илья', 'Лёва')
    unusual_female_names = ('Любовь')
    result_of_boys = {}
    result_of_girls = {}

    with open(filepath, 'r', encoding='cp1251') as file:
        last_year = 0

        for string in file:
            fullname = ''
            year = ''
            first_name_index = string.find('/">')
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
                if name[-1] == 'а' or name[-1] == 'я' or \
                        name in unusual_female_names:
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


def extract_general(stat):
    answer_list = []
    general_girl_stat = {}
    general_boy_stat = {}

    girls_dict = stat['girls_stat']
    boys_dict = stat['boys_stat']

    years = sorted(
        list(stat['girls_stat'].keys()) or list(stat['boys_stat'].keys()))
    for key in years:
        for i in girls_dict[key].keys():
            if i in general_girl_stat.keys():
                general_girl_stat[i] += girls_dict[key][i]
            else:
                general_girl_stat[i] = girls_dict[key][i]

        for k in boys_dict[key].keys():
            if k in general_boy_stat.keys():
                general_boy_stat[k] += boys_dict[key][k]
            else:
                general_boy_stat[k] = boys_dict[key][k]

    for key in general_girl_stat:
        answer_list.append((key, general_girl_stat[key]))
    for key in general_boy_stat:
        answer_list.append((key, general_boy_stat[key]))
    return sorted(answer_list, key=lambda x: x[1], reverse=True)


def extract_general_male(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён мальчиков.
    Список должен быть отсортирован по убыванию количества.
    """
    answer_list = []
    general_boy_stat = {}

    boys_dict = stat['boys_stat']
    for key in extract_years(stat):
        for i in boys_dict[key].keys():
            if i in general_boy_stat.keys():
                general_boy_stat[i] += boys_dict[key][i]
            else:
                general_boy_stat[i] = boys_dict[key][i]

    for key in general_boy_stat:
        answer_list.append((key, general_boy_stat[key]))
    return sorted(answer_list, key=lambda x: x[1], reverse=True)


def extract_general_female(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён девочек.
    Список должен быть отсортирован по убыванию количества.
    """
    answer_list = []
    general_girl_stat = {}

    girls_dict = stat['girls_stat']
    for key in extract_years(stat):
        for i in girls_dict[key].keys():
            if i in general_girl_stat.keys():
                general_girl_stat[i] += girls_dict[key][i]
            else:
                general_girl_stat[i] = girls_dict[key][i]

    for key in general_girl_stat:
        answer_list.append((key, general_girl_stat[key]))

    return sorted(answer_list, key=lambda x: x[1], reverse=True)


def extract_year(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    answer_list = []
    general_girl_stat = {}
    general_boy_stat = {}

    girls_dict = stat['girls_stat']
    boys_dict = stat['boys_stat']

    key = year
    for i in girls_dict[key].keys():
        if i in general_girl_stat.keys():
            general_girl_stat[i] += girls_dict[key][i]
        else:
            general_girl_stat[i] = girls_dict[key][i]

    for i in boys_dict[key].keys():
        if i in general_boy_stat.keys():
            general_boy_stat[i] += boys_dict[key][i]
        else:
            general_boy_stat[i] = boys_dict[key][i]

    for key in general_girl_stat:
        answer_list.append((key, general_girl_stat[key]))
    for key in general_boy_stat:
        answer_list.append((key, general_boy_stat[key]))
    return sorted(answer_list, key=lambda x: x[1], reverse=True)


def extract_year_male(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён мальчиков в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    answer_list = []
    general_boy_stat = {}
    boys_dict = stat['boys_stat']
    key = year

    for i in boys_dict[key].keys():
        if i in general_boy_stat.keys():
            general_boy_stat[i] += boys_dict[key][i]
        else:
            general_boy_stat[i] = boys_dict[key][i]

    for key in general_boy_stat.keys():
        answer_list.append((key, general_boy_stat[key]))

    return sorted(answer_list, key=lambda x: x[1], reverse=True)


def extract_year_female(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён девочек в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    answer_list = []
    general_girl_stat = {}
    girls_dict = stat['girls_stat']

    for i in girls_dict[year].keys():
        if i in general_girl_stat.keys():
            general_girl_stat[i] += girls_dict[year][i]
        else:
            general_girl_stat[i] = girls_dict[year][i]

    for key in general_girl_stat.keys():
        answer_list.append((key, general_girl_stat[key]))

    return sorted(answer_list, key=lambda x: x[1], reverse=True)