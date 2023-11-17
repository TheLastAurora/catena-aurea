from ..crawler import get_page
import logging
import os
from bs4 import BeautifulSoup
import re
import json


log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(filename=os.path.join(log_dir, 'extract.log'), format='%(asctime)s %(message)s', level=logging.ERROR, filemode='w')

class NoReferencesError(Exception):
    def __init__(self, pattern):
        self.message = f'[URL_REFERENCE] Failed to retrieve any url references for the given pattern: "{pattern}".'
        super().__init__(self.message)

class EmptyPageError(Exception):
    def __init__(self):
        self.message = f'[CONTENT] Failed to retrieve content.'
        super().__init__(self.message)

def extract(pattern: str) -> dict:
    """Extracts content for page given a pattern"""
    def extract_refs():
        try:
            pattern = re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {pattern}") from e
        refs = {}
        with open(os.path.join(os.path.dirname(__file__), '../../output/output.json'), mode='r') as f:
            for line in f:
                refs.update(json.loads(re.search(pattern, line).group(0)))
        if not refs:
            err = NoReferencesError(pattern)
            logging.error(err.message)
            raise err
        return refs

    def extract_base_content(refs: dict) -> str:
        for url in refs.keys():
            
            # Divides the content of the page based on the page HTML three types: index, subindex, content.

            content = get_page(url).find(class_='row')

            if not content:
                err = EmptyPageError()
                logging.error(err.message)
                raise err
            yield content

    content = extract_base_content(extract_refs())
    return content

