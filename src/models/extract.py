from crawler import get_page
from unicodedata import normalize
from copy import copy
from bs4 import BeautifulSoup
from typing import Generator
import logging
import os
import re
import json


log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "extract.log"),
    format="%(asctime)s %(message)s",
    level=logging.ERROR,
    filemode="w",
)


class NoReferencesError(Exception):
    def __init__(self, pattern):
        self.message = f'[URL_REFERENCE] Failed to retrieve any matching references for the given pattern: "{pattern}".'
        super().__init__(self.message)


class EmptyPageError(Exception):
    def __init__(self):
        self.message = f"[CONTENT] Failed to retrieve content."
        super().__init__(self.message)


def extract_refs(word: str) -> dict:
    """Tries to match the given url pattern to the references"""
    try:
        pattern = re.compile(f'.*{word}.*')
    except re.error as e:
        raise ValueError(f"Invalid regex pattern: {pattern}") from e
    refs = {}
    with open(os.path.join(os.path.dirname(__file__), "../output/output.json"), mode="r") as f:
        for line in f:
            line = '{' + line.strip()[:-1] + '}'
            try:
                if re.search(pattern, line):
                    refs.update(json.loads(line))
            except:
                pass
    if not refs:
        err = NoReferencesError(pattern.pattern)
        logging.error(err.message)
        raise err
    return refs


def extract_raw_content(refs: dict) -> Generator:
    """Yields and divides the content of the page based on the page HTML three types: index, subindex, content for each url."""
    for url in refs.keys():
        _pg = BeautifulSoup(get_page(url), 'html.parser')
        core = _pg.find('div', {'id': "content"})
        if not core:
            err = EmptyPageError()
            logging.error(err.message)
            continue

        # Formatter
        SYMBOLS = str.maketrans("", "", "<>*0123456789.")

        def format(x):
            return x.text.translate(SYMBOLS).strip()

        # Index
        if core.select("#glossa_ordinaria"):
            yield {
                "tittle": format(core.select_one("h4")),
                "section": [format(s) for s in core.select("nav > ul > li > a")],
            }

        # Subindex
        elif core.select(".edition_intro"):
            yield {
                "section": format(core.select_one("h1")),
                "subsection": [s.text for s in core.select(".corps-edition ul li a")],
            }

        # Core content
        elif core.select("#textContainer"):
            cnt = core.find_all("div", {'class': ['verset', re.compile('.*unite_textuelle.*')]})
            content = []
            for _c in cnt:
                c = copy(_c)
                if c["class"][0] == "verset":
                    content.append({"verset": str, "unite_textuelle": []}) # Each element of this new list is a set of verses
                    for s in c.find_all("span"):
                        s.decompose()
                        content[-1]["verset"] = normalize("NFKD", c.text.strip())
                else:
                    content[-1]["unite_textuelle"].append(normalize("NFKD", c.text))
            if content:
                # TODO: Fix content append.
                yield {
                    "section": format(core.select_one("#textContainer .titre_edition")),
                    "subsection": core.select_one("#textContainer h2").text,
                    "content": {[*content]},
                }

def extract(word: str) -> dict:
    core = extract_raw_content(extract_refs(word))
    return core
