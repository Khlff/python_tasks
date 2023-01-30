import argparse
import itertools
import os
import pathlib
import re
import signal
import sys
import time
import urllib.request
import threading
from typing import Optional
from urllib.error import URLError, HTTPError

exit_event = threading.Event()


def load_content(url: str) -> Optional[str]:
    try:
        return urllib.request.urlopen(url, timeout=10).read().decode("UTF-8")
    except (HTTPError, URLError):
        return None


def extract_articles_by_page_number(page_number):
    base_link = 'https://habr.com'
    page_content = load_content(f"https://habr.com/ru/all/page{page_number}/")
    links_of_articles = re.findall(r'href="(.*?)" data-article-link',
                                   page_content)
    return [base_link + i for i in links_of_articles]


def normalize_file_name(raw_filename):
    raw_filename = raw_filename.replace(' ', '_')
    raw_filename = raw_filename.replace(':', '.')
    raw_filename = raw_filename.replace('?', '.')
    raw_filename = raw_filename.replace('\\', '.')
    raw_filename = raw_filename.replace('/', '.')
    raw_filename = raw_filename.replace('*', '.')
    raw_filename = raw_filename.replace('"', '_')
    raw_filename = raw_filename.replace('<', '_')
    raw_filename = raw_filename.replace('>', '_')
    raw_filename = raw_filename.replace('|', '_')
    return raw_filename


def extract_article_photos(link):
    page_content = load_content(link)

    article_name_find = re.findall(
        r'<h1 lang="ru" class="tm-article-snippet__title '
        r'tm-article-snippet__title_h1"><span>(.*?)</span></h1>',
        page_content)

    article_name = article_name_find[0] \
        if article_name_find else 'name_not_found'
    article_name = normalize_file_name(article_name)

    links_of_articles = re.findall(r'img src="(https://habrastorage.org/.*?)"',
                                   page_content)

    return {article_name: links_of_articles}


def download_pictures(url_dict: dict, out_dir: pathlib.Path):
    if len(list(url_dict.values())[0]) != 0:
        article_name = list(url_dict.keys())[0]
        article_path = os.path.join(out_dir, article_name)

        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        if not os.path.exists(article_path):
            os.mkdir(article_path)

        for picture_url in url_dict[article_name]:
            picture_data = urllib.request.urlopen(picture_url,
                                                  timeout=20).read()
            filename = picture_url.split("/")[-1]
            out = open(article_path + f"/{filename}", 'wb')
            out.write(picture_data)
            out.close()
    else:
        print('В статье нет картинок')


def signal_handler(signal, frame):
    print('Interrupt!')
    exit_event.set()


def run_scraper(threads: int, articles: int, out_dir: pathlib.Path) -> None:
    threads_list = []
    signal.signal(signal.SIGINT, signal_handler)

    timestamp = time.time()
    print('Собираю список статей')
    links_list = extract_articles_by_page_number(1)

    page_number = 1
    while len(links_list) < articles:
        page_number += 1
        links_of_page = extract_articles_by_page_number(page_number)
        links_list = list(itertools.chain(links_list, links_of_page))

    for link_number in range(articles):
        url_dict = extract_article_photos(links_list[link_number])

        if exit_event.is_set():
            [thread.join() for thread in threads_list]
            sys.exit(1)

        if threading.active_count() - 1 < threads:
            print('[threading] Место есть, создаю поток')
            thread = threading.Thread(target=download_pictures,
                                      args=(url_dict, out_dir,))
            thread.start()
            threads_list.append(thread)

        else:
            while threading.active_count() - 1 == threads:
                print('[threading] Места нет')
                time.sleep(0.1)
            else:
                print(
                    '[threading] Место для потока освободилось, создаю поток')
                thread = threading.Thread(target=download_pictures,
                                          args=(url_dict, out_dir,))
                thread.start()
                threads_list.append(thread)

    for thread in threads_list:
        thread.join()

    print(f"Время на парсинг: {time.time() - timestamp}")


def main():
    script_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(
        usage=f'{script_name} [ARTICLES_NUMBER] THREAD_NUMBER OUT_DIRECTORY',
        description='Habr parser',
    )
    parser.add_argument(
        '-n', type=int, default=25, help='Number of articles to be processed',
    )
    parser.add_argument(
        'threads', type=int, help='Number of threads to be run',
    )
    parser.add_argument(
        'out_dir', type=pathlib.Path, help='Directory to download habr images',
    )
    args = parser.parse_args()

    run_scraper(args.threads, args.n, args.out_dir)


if __name__ == '__main__':
    main()
