from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests_html import HTMLSession
from pprint import pprint
import json
import concurrent.futures
import logging
import os
import re

# TODO: Implementar multithreading

cwd = os.path.dirname(__file__)
log_dir = os.path.join(cwd, 'logs')
out_dir = os.path.join(cwd, 'ouput')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

logging.basicConfig(filename=os.path.join(log_dir, 'crawler.log'), format='%(asctime)s %(message)s', level=logging.ERROR, filemode='w')
index = 'https://gloss-e.irht.cnrs.fr/php/livres-liste.php?id=catena'


def get_page(url: str) -> str:
    try:
        session = HTMLSession()
        res = session.get(url, timeout=5)
        if res.status_code != 200:
            raise
        return res.text
    except Exception as re:
        logging.error(f'Failed to handle request for {url}.')
        return ""


def crawl(page: str, base: str) -> dict:
    content = BeautifulSoup(page, 'html.parser')
    refs = content.find_all('a')
    mapping = {urljoin(base, r.get('href')): r.get_text() for r in refs}
    return mapping


def crawler(index: str, *args, depth=2) -> dict:
    index_page = get_page(index)
    mapping = crawl(index_page, base=index)
    visited = set()
    for _ in range(depth):
        to_visit = {}
        for url in mapping.keys():
            if url not in visited:
                to_visit.update(crawl(page=get_page(url), base=index))
                visited.add(url)
        mapping.update(to_visit)
    return mapping


with open(os.path.join(out_dir, 'output.json'), 'w', encoding='utf-8') as f:
    data = crawler(index)
    json.dump(data, f)
