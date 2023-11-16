from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests_html import HTMLSession
import asyncio
import json
import logging
import os


cwd = os.path.dirname(__file__)
log_dir = os.path.join(cwd, 'logs')
out_dir = os.path.join(cwd, 'ouput')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

logging.basicConfig(filename=os.path.join(log_dir, 'crawler.log'), format='%(asctime)s %(message)s', level=logging.ERROR, filemode='w')



def get_page(url: str) -> str:
    """Connects to URL page and returns its html in str."""
    try:
        session = HTMLSession()
        res = session.get(url, timeout=5)
        if res.status_code != 200:
            raise
        return res.text
    except Exception as re:
        logging.error(f'[REQUEST] Failed to handle request for {url}.')
        return ""


def _crawl(page: str, base: str) -> dict:
    """Gather all the references from page and return its mapping in the form of "url": "inner_text"."""
    content = BeautifulSoup(page, 'html.parser')
    refs = content.find_all('a')
    mapping = {urljoin(base, r.get('href')): r.get_text() for r in refs}
    return mapping

async def crawler_async(url: str, visited: set, to_visit: dict) -> dict:
    if url not in visited:
                to_visit.update(_crawl(page=get_page(url), base=index))
                visited.add(url)

async def crawl(index: str, *args, depth=2) -> dict:
    """Executes the crawl operation for the given index at certain depth, returning all the references."""
    index_page = get_page(index)
    mapping = _crawl(index_page, base=index)
    visited = set()
    for _ in range(depth):
        to_visit = {}
        tasks = []
        for url in mapping.keys():
            tasks.append(asyncio.create_task(crawler_async(url, visited, to_visit)))
        await asyncio.gather(*tasks)
        mapping.update(to_visit)
    return mapping


if __name__ == "__main__":
    index = 'https://gloss-e.irht.cnrs.fr/php/livres-liste.php?id=catena'
    data = asyncio.run(crawl(index))
    if data:
        with open(os.path.join(out_dir, 'output.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f)
            print('Crawler finished with success.')
    else:
        raise Exception('Failed to execute crawling routine!')