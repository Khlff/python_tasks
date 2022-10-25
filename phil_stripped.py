import sys
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
        return result.read().decode(
            result.headers.get_content_charset()).replace('\n', '')

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

    result_of_search = (
        re.search(
            r'<div id="content" class="mw-body" role="main">(.*)</div><div '
            r'id="mw-navigation">',
            page))

    return (result_of_search.start(),
            result_of_search.end()) if result_of_search is not None else (0, 0)


def extract_links(page, begin, end):
    """
    Функция принимает на вход содержимое страницы и начало и конец интервала,
    задающего позицию содержимого статьи на странице и возвращает все имеющиеся
    ссылки на другие вики-страницы без повторений и с учётом регистра.
    """

    links_list = re.findall(
        r'[hH][rR][eE][fF]=[\'\"]/wiki/([\w%\(\)\_\,]*)[\'\"]',
        page[begin:end])

    normalized_links = []
    for link in links_list:
        link = parse.unquote(link)
        if link is not None and link not in normalized_links:
            normalized_links.append(link)

    return normalized_links


def find_way(dict_of_sites_names, what_to_find):
    list_of_path = [what_to_find]
    temp_site = what_to_find

    while temp_site in dict_of_sites_names.keys():
        temp_site = dict_of_sites_names[temp_site]
        list_of_path.append(temp_site)

    list_of_path.reverse()
    return list_of_path


def find_chain(start, finish):
    """
    Функция принимает на вход название начальной и конечной статьи и возвращает
    список переходов, позволяющий добраться из начальной статьи в конечную.
    Первым элементом результата должен быть start, последним — finish.
    Если построить переходы невозможно, возвращается None.
    """

    if start == finish:
        return [start]

    start = start.replace(' ', '_')
    finish = finish.replace(' ', '_')

    list_of_used_links = [start]
    table_of_links = {}
    queue = [start]

    while queue:
        link_from_queue = queue.pop(0)
        content_of_queue_page = get_content(link_from_queue)
        if content_of_queue_page is None:
            continue
        start_of_content, end_of_content = extract_content(
            content_of_queue_page)
        links_of_queue_page = extract_links(content_of_queue_page,
                                            start_of_content, end_of_content)

        for link in links_of_queue_page:
            if link not in list_of_used_links:
                queue.append(link)
                table_of_links[link] = link_from_queue
                list_of_used_links.append(link)
            if link == finish:
                return find_way(table_of_links, finish)


def main():
    args = sys.argv
    if len(args) == 3:
        start_point = args[1]
        end_point = args[2]
    else:
        return None
    print(find_chain(start_point, end_point))


if __name__ == '__main__':
    main()
