import argparse
import itertools
import os
import pathlib
import sys
import urllib.request
from typing import Optional
from urllib.error import URLError, HTTPError
import re


def load_content(url: str) -> Optional[str]:
    try:
        return urllib.request.urlopen(url, timeout=10).read().decode("UTF-8")
    except (HTTPError, URLError):
        return None


def extract_articles_url(page_number):
    base_link = 'https://habr.com'
    page_content = load_content(f"https://habr.com/ru/all/page{page_number}/")
    links_of_articles = re.findall(r'href="(.*?)" data-article-link',
                                   page_content)
    return [base_link + i for i in links_of_articles]


def extract_article_photos(link, directory='.'):
    page_content = load_content(link)
    article_name = re.findall(
        r'<h1 lang="ru" class="tm-article-snippet__title '
        r'tm-article-snippet__title_h1"><span>(.*?)</span></h1>',
        page_content)[0]
    print(page_content)
    links_of_articles = re.findall(r'img src="(https:.*?\.)"',
                                   page_content)
    # https: // .jpg
    return {article_name: links_of_articles}


def run_scraper(threads: int, articles: int, out_dir: pathlib.Path) -> None:
    links_list = extract_articles_url(1)

    page_number = 1
    while len(links_list) < articles:
        page_number += 1
        links_of_page = extract_articles_url(page_number)
        links_list = list(itertools.chain(links_list, links_of_page))

    for link_number in range(articles):
        print(extract_article_photos(links_list[link_number]))


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
