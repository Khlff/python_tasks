#!/usr/bin/env python3
import re
from urllib import request, parse, error


def get_content(name):
    """
    Функция возвращает содержимое вики-страницы name из русской Википедии.
    В случае ошибки загрузки или отсутствия страницы возвращается None.
    """
    try:
        url = 'https://ru.wikipedia.org/wiki/' + parse.quote(name)
        result = request.urlopen(url)
        return result.read().decode(result.headers.get_content_charset()).replace('\n', '')
    except error.HTTPError:
        return None
    except error.URLError:
        return None


def extract_content(page):
    """
    Функция принимает на вход содержимое страницы и возвращает 2-элементный
    tuple, первый элемент которого — номер позиции, с которой начинается
    содержимое статьи, второй элемент — номер позиции, на котором заканчивается
    содержимое статьи.
    Если содержимое отсутствует, возвращается (0, 0).
    """

    if page is None:
        return (0, 0)

    resultOfSearch = \
        re.findall(r'<div id="content" class="mw-body" role="main">(.*)</div><div id="mw-navigation">', page)[0]

    return resultOfSearch if resultOfSearch != '' else (0, 0)

    # first_index = page.find('class="vector-body">') - 20
    # if first_index == -21:
    #     return (0, 0)
    # second_index = page.find('<div id="mw-navigation">')
    # return page[first_index:second_index]


# print(extract_content(get_content('Ящерицы')))
extract_content(get_content('Ящерицы'))


def extract_links(page, begin, end):
    """
    Функция принимает на вход содержимое страницы и начало и конец интервала,
    задающего позицию содержимого статьи на странице и возвращает все имеющиеся
    ссылки на другие вики-страницы без повторений и с учётом регистра.
    """



def find_chain(start, finish):
    """
    Функция принимает на вход название начальной и конечной статьи и возвращает
    список переходов, позволяющий добраться из начальной статьи в конечную.
    Первым элементом результата должен быть start, последним — finish.
    Если построить переходы невозможно, возвращается None.
    """
    pass


def main():
    pass


if __name__ == '__main__':
    main()
