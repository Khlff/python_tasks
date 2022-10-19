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

    result_of_search = \
        re.search(r'<div id="content" class="mw-body" role="main">(.*)</div><div id="mw-navigation">', page)

    return (result_of_search.start(), result_of_search.end()) if result_of_search is not None else (0, 0)


def extract_links(page, begin, end):
    """
    Функция принимает на вход содержимое страницы и начало и конец интервала,
    задающего позицию содержимого статьи на странице и возвращает все имеющиеся
    ссылки на другие вики-страницы без повторений и с учётом регистра.
    """
    links_list = re.findall(r'<a href="/wiki/(.*?)"', page[begin:end])
    return links_list


def find_chain(start, finish):
    """
    Функция принимает на вход название начальной и конечной статьи и возвращает
    список переходов, позволяющий добраться из начальной статьи в конечную.
    Первым элементом результата должен быть start, последним — finish.
    Если построить переходы невозможно, возвращается None.
    """
    if start == finish:
        return [start]
    content = get_content(start)
    begin, end = extract_content(content)
    links = extract_links(content, begin, end)
    table_of_links = {}
    for link in links:
        if start in table_of_links.keys():
            table_of_links[start].append(link)
        else:
            table_of_links[start] = [link]

    while links:
        name_of_page = links.pop(0)
        new_page = get_content(name_of_page)
        if new_page is None:
            continue
        new_page_content = extract_content(new_page)
        new_page_content_links = extract_links(new_page, new_page_content[0], new_page_content[1])
        print(parse.unquote(name_of_page))
        if new_page == finish:
            return "ты пидор"
        for link in new_page_content_links:

            if new_page in table_of_links.keys():
                table_of_links[new_page].append(parse.unquote(link))
            else:
                table_of_links[new_page] = [parse.unquote(link)]
    print(table_of_links)


def main():
    content = get_content('Ящерицы')
    begin, end = extract_content(content)
    links = extract_links(content, begin, end)
    find_chain('Ящерицы', 'Животные')


if __name__ == '__main__':
    main()
