from ..crawler import get_page
from unicodedata import normalize
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


def extract_refs(pattern: str) -> dict:
    """Tries to match the given url pattern to the references"""
    try:
        pattern = re.compile(pattern)
    except re.error as e:
        raise ValueError(f"Invalid regex pattern: {pattern}") from e
    refs = {}
    with open(
        os.path.join(os.path.dirname(__file__), "../../output/output.json"), mode="r"
    ) as f:
        for line in f:
            refs.update(json.loads(re.search(pattern, line).group(0)))
    if not refs:
        err = NoReferencesError(pattern)
        logging.error(err.message)
        raise err
    return refs


def extract_raw_content(refs: dict) -> Generator:
    """Yields and divides the content of the page based on the page HTML three types: index, subindex, content for each url."""
    for url in refs.keys():
        content = get_page(url).find("content")
        if not content:
            err = EmptyPageError()
            logging.error(err.message)
            raise err

        # Formatter
        SYMBOLS = str.maketrans("", "", "<>*0123456789.")

        def format(x):
            return x.text.translate(SYMBOLS).strip()

        # Index
        if content.select("#glossa_ordinaria"):
            yield {
                "tittle": format(content.select_one("h4")),
                "section": [format(s) for s in content.select("nav > ul > li > a")],
            }

        # Subindex
        elif content.select(".edition_intro"):
            yield {
                "section": format(content.select_one("h1")),
                "subsection": [
                    s.text for s in content.select(".corps-edition ul li a")
                ],
            }

        # Core content
        elif content.select("#textContainer"):
            
            # Formating the versets
            vs = content.select("#textContainer .edition .verset")
            norm_versets = []
            for v in vs:
                for s in v.find_all('span'):
                    s.decompose()
                v = normalize("NFKD", v.text)
                norm_versets.append(v)

            # Formating the unite_textuelles
            vs = content.select("#textContainer .edition .unite_textuelle")

            norm_ut = []
            for ut in vs:
                ut = normalize("NFKD", ut.text)
                norm_ut.append(ut)


            yield {
                "section": format(content.select_one("#textContainer .titre_edition")),
                "subsection": content.select_one("#textContainer h2").text,
                "content": {}
            }

        yield None


def extract(pattern: str) -> dict:
    content = extract_raw_content(extract_refs(pattern))
    return content
