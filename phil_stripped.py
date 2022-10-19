import datetime
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

    result_of_search = \
        re.search(
            r'<div id="content" class="mw-body" role="main">(.*)</div><div '
            r'id="mw-navigation">',
            page)

    return (result_of_search.start(),
            result_of_search.end()) if result_of_search is not None else (0, 0)


def extract_links(page, begin, end):
    """
    Функция принимает на вход содержимое страницы и начало и конец интервала,
    задающего позицию содержимого статьи на странице и возвращает все имеющиеся
    ссылки на другие вики-страницы без повторений и с учётом регистра.
    """
    links_list = re.findall(r'href="/wiki/([\w%\(\)\_]*)"',
                            page[begin:end])  # тут срёт из-за %, . и тд
    normalized_links = []
    for link in links_list:
        link = parse.unquote(link)
        if link is not None and link not in normalized_links:
            normalized_links.append(link)
    return normalized_links


def get_name_of_article(content):
    if content == None:
        names = None
    else:
        names = re.findall(r'<span class="mw-page-title-main">(.*?)</span>',
                           content)
    name = names[0].replace(' ', '_') if names else None
    return name


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
    finish = start.replace(' ', '_')

    list_of_used_links = [start]
    table_of_links = {start: []}
    queue = []

    content_of_start_page = get_content(start)
    start_of_content, end_of_content = extract_content(content_of_start_page)
    links_of_start_page = extract_links(content_of_start_page,
                                        start_of_content, end_of_content)

    for link in links_of_start_page:
        if link not in list_of_used_links:
            table_of_links[start].append(link)
            list_of_used_links.append(link)
            queue.append(link)
        if link == finish:
            return table_of_links

    while queue:
        link_from_queue = queue.pop(0)
        content_of_queue_page = get_content(link_from_queue)
        start_of_content, end_of_content = extract_content(
            content_of_queue_page)
        links_of_queue_page = extract_links(content_of_queue_page,
                                            start_of_content, end_of_content)

        table_of_links[link_from_queue] = []
        for link in links_of_queue_page:
            if link not in list_of_used_links:
                queue.append(link)
                table_of_links[link_from_queue].append(link)
                list_of_used_links.append(link)
            if link == finish:
                return table_of_links


def main():
    first = datetime.datetime.now()
    print(find_chain('Путин,_Владимир_Владимирович', 'Президент'))
    second = datetime.datetime.now()
    print(second-first)

if __name__ == '__main__':
    main()
