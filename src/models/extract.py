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


def extract_refs(word: str = None, interval: list[str] = None) -> dict:
    """Tries to match the given url pattern to the references"""
    refs = {}
    with open(os.path.join(os.path.dirname(__file__), "../output/output.json"), mode="r") as f:
        if word:
            try:
                pattern = re.compile(f".*{word}.*", re.IGNORECASE)  # Gets the whole line
            except re.error as e:
                raise ValueError(f"Invalid regex pattern: {pattern}") from e
            for line in f:
                line = "{" + line.strip()[:-1] + "}"  # Format the line to support json loading
                try:
                    if re.search(pattern, line):
                        refs.update(json.loads(line))
                except:
                    pass
        elif len(interval) == 2:
            start, end = interval
            try:
                start_pattern = re.compile(f".*{start}.*")
                end_pattern = re.compile(f".*{end}.*")
            except re.error as e:
                raise ValueError(f"Invalid regex pattern: {pattern}") from e

            inside_interval = False
            for line in f:
                line = "{" + line.strip()[:-1] + "}"  # Format the line to support json loading
                try:
                    if re.search(start_pattern, line):
                        inside_interval = True
                        refs.update(json.loads(line))
                    elif inside_interval and re.search(end_pattern, line):
                        inside_interval = False
                        refs.update(json.loads(line))
                        break  # Stop reading once the end pattern is found within the interval
                    elif inside_interval:
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
        _pg = BeautifulSoup(get_page(url), "html.parser")
        core = _pg.find("div", {"id": "content"})
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
            rgxs = {
                "ut": re.compile(".*unite_textuelle.*"),
                "vst": re.compile("verset.*"),
                "hx": re.compile("h[2-4]"),
            }
            cnt = core.find_all("div", {"class": [rgxs.get("ut"), rgxs.get("vst")]})  # Gets only for the versets and the texts
            h_tag = core.find_all(rgxs.get("hx"))[-1] # Looks if there is any header
            vst_present = any([bool(c.find_all("div", {"class": rgxs.get("vst")})) for c in cnt])  # Checks whether or not there are headers (html tag headers or class versets)
            if (cnt and not vst_present):  # No versets, but there can be html headers, like in: https://gloss-e.irht.cnrs.fr/php/editions_chapitre.php?id=biblia&numLivre=79&chapitre=79_Prol.2b
                cnt = core.find_all("div", {"class": rgxs.get("ut")})
                if h_tag:
                    cnt.insert(0, h_tag)
            
            cnt = list(filter(lambda c: "groupe_verset" not in c.get("class"), cnt))  # Deletes all group_verset like in the latest example
            content = []
            for _c in cnt:
                c = copy(_c)
                _isheader = any(re.match(rgx, c.get('class')[0]) for rgx in [rgxs.get("vst"), rgxs.get("hx")])  # Checks if this component is a header
                # Fix logic
                if _isheader:
                    content.append({"verset": str, "unite_textuelle": []})  # Each element of this new list is a set of verses
                    for s in c.find_all("span"):
                        s.decompose()
                        content[-1]["verset"] = normalize("NFKD", c.text.strip())
                else:
                    if content:  # No headers found.
                        content[-1]["unite_textuelle"].append(normalize("NFKD", c.text))
            if content:
                yield {
                    "section": format(core.select_one("#textContainer .titre_edition")),
                    "subsection": core.select_one("#textContainer h2").text,
                    "content": [*content],
                }


def extract(*args, **kwargs) -> dict:
    """Effectively executes the extraction of the data"""
    refs = extract_refs(*args, **kwargs)
    core = extract_raw_content(refs)
    return core
