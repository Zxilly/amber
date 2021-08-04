from usp.tree import sitemap_tree_for_homepage
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import requests


def archive_request(url: str):
    print(f"request {url}")
    requests.get(f"https://web.archive.org/save/{url}")


def archive(target: str):
    tree = sitemap_tree_for_homepage(target)

    urls = set()

    for page in tree.all_pages():
        urls.add(page.url)

    with ThreadPoolExecutor(max_workers=8) as t:
        result_list = []
        for url in urls:
            result = t.submit(archive_request, url)
            result_list.append(result)

        as_completed(result_list)
    print('archived')


if __name__ == '__main__':
    try:
        target = sys.argv[1]
        archive(target)
    except IndexError:
        print('Plz use url of your site as argument.')
