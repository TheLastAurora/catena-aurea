# from ..crawler import get_page
import logging
import os
import bs4
import re
import json

cwd = os.getcwd()
log_dir = os.path.join(cwd, 'logs')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(filename=os.path.join(log_dir, 'extract.log'), format='%(asctime)s %(message)s', level=logging.ERROR, filemode='w')

class NoReferencesError(Exception):
    def __init__(self, pattern):
        self.message = f'[PATTERN] Failed to retrieve any references for the given pattern: "{pattern}".'
        super().__init__(self.message)


def extract(pattern: str) -> dict:
    """Extracts links """
    def extract_refs():
        try:
            pattern = re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {pattern}") from e
        refs = {}
        with open(os.path.join(os.path.dirname(__file__), '../../output/output.json'), mode='r') as f:
            for line in f:
                refs.update(json.loads(re.search(pattern, line).group(0)))
        return refs
    refs = extract_refs()
    if not refs:
        err = NoReferencesError(pattern)
        logging.error(err.message)
        raise err
    # Todo implement 
