from config.config import get_logger, get_input
from aiohttp import ClientSession, ClientTimeout
from unicodedata import normalize
from bs4 import BeautifulSoup
from typing import Generator
from copy import copy
import asyncio
import json
import re


FORMATER_SYMBOLS = str.maketrans("", "", "<>*0123456789.")


logger = get_logger('extract')


class NoReferencesError(Exception):
    def __init__(self, pattern):
        self.message = f'[URL_REFERENCE] Failed to retrieve any matching references for the given pattern: "{pattern}".'
        super().__init__(self.message)


class EmptyPageError(Exception):
    def __init__(self, msg=None):
        self.message = "[CONTENT] Failed to retrieve page content." if not msg else f"[CONTENT] {msg}"
        super().__init__(self.message)


async def get_page(url: str) -> str:
    """Connects to URL page and returns its html in str."""
    timeout = ClientTimeout(total=60)
    async with ClientSession(timeout=timeout) as session:
        try:
            async with session.get(url) as res:
                if res.status != 200:
                    raise Exception(f"Failed to get {url}: {res.status}")
                return await res.text()
        except Exception as e:
            logger.warning(f'[REQUEST] Failed to handle request for {url}.')
            return ""


def extract_refs(word: str = None, interval: list[str] = None) -> dict:
    """Tries to match the given url pattern to the references"""
    refs = {}
    filename, encoding = get_input('crawl_index')
    with open(file=filename, encoding=encoding, mode='r') as f:
        if word:
            try:
                # Gets the whole line
                pattern = re.compile(f".*{word}.*", re.IGNORECASE)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern: {pattern}") from e
            for line in f:
                # Format the line to support json loading
                line = "{" + line.strip()[:-1] + "}"
                try:
                    if re.search(pattern, line):
                        refs.update(json.loads(line))
                except:
                    pass
        elif interval and len(interval) == 2:
            start, end = interval
            try:
                start_pattern = re.compile(f".*{start}.*")
                end_pattern = re.compile(f".*{end}.*")
            except re.error as e:
                raise ValueError(f"Invalid regex pattern: {pattern}") from e

            inside_interval = False
            for i, line in enumerate(f.readlines()):
                # Format the line to support json loading
                line = "{" + line.strip()[:-1] + "}"
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
        err = NoReferencesError("")
        logger.error(err.message)
        raise err
    return refs


def _format(x):
    return x.text.translate(FORMATER_SYMBOLS).strip()


def _type_index(core: BeautifulSoup) -> dict:
    return {
        "tittle": _format(core.select_one("h4")),
        "section": [_format(s) for s in core.select("nav > ul > li > a")],
    }


def _type_subindex(core: BeautifulSoup) -> dict:
    return {
        "section": _format(core.select_one("h1")),
        "subsection": [s.text for s in core.select(".corps-edition ul li a")],
    }


def _type_paragraph(core: BeautifulSoup) -> dict:
    rgxs = {
        "ut": re.compile(".*unite_textuelle.*"),
        "vst": re.compile("verset.*"),
        "hx": re.compile("h[2-4]"),
    }

   # Gets only for the versets and the texts
    cnt = core.find_all(
        "div", {"class": [rgxs.get("ut"), rgxs.get("vst")]})

    h_tag = core.find_all(rgxs.get("hx"))[-1]  # Looks if there is any header
    # Checks whether or not there are headers (html tag headers or class versets)
    _vst_present = any(
        [bool(c.find_all("div", {"class": rgxs.get("vst")})) for c in cnt])
    if (cnt and not _vst_present):  # No versets, but there can be html headers, like in: https://gloss-e.irht.cnrs.fr/php/editions_chapitre.php?id=biblia&numLivre=79&chapitre=79_Prol.2b
        cnt = core.find_all("div", {"class": rgxs.get("ut")})
        if h_tag:
            cnt.insert(0, h_tag)

    # Deletes all group_verset like in the latest example
    cnt = [cnt[0]] + \
        list(filter(lambda c: "groupe_verset" not in c.get("class"), cnt[1:]))
    content = []

    if h_tag:  # This comes with an h tag element and the rest is unite_textuelle.
        content.append({"verset": str, "unite_textuelle": []})
        content[-1]["verset"] = normalize("NFKD", cnt[0].text.strip())
        for _c in cnt[1:]:
            c = copy(_c)
            content[-1]["unite_textuelle"].append(
                normalize("NFKD", c.text))
    else:  # No h tag elements, but versets.
        for _c in cnt:
            c = copy(_c)
            # Checks if this component is a verset element
            _isverset = any(re.match(rgx, c.get('class')[
                            0]) for rgx in [rgxs.get("vst")])
            if _isverset:  # Each element of this new list is a set of verses
                content.append({"verset": str, "unite_textuelle": []})
                for s in c.find_all("span"):
                    s.decompose()
                    content[-1]["verset"] = normalize(
                        "NFKD", c.text.strip())

            else:  # Its a unite_textuelle
                content[-1]["unite_textuelle"].append(
                    normalize("NFKD", c.text))
    return {
        "section": _format(core.select_one("#textContainer .titre_edition")),
        "subsection": core.select_one("#textContainer h2").text,
        "content": [*content],
    } if content else None


def extract_raw_content(refs: dict) -> Generator:
    """Yields and breaks the content of the page based on the page HTML three types: index, subindex, content for each url."""

    async def get_pages():
        tasks = [asyncio.create_task(get_page(url)) for url in refs.keys()]
        pages = await asyncio.gather(*tasks)
        return pages

    pages = asyncio.run(get_pages())
    if not any(pages):
        err = EmptyPageError("No pages avaliable for extraction. Please, ensure the webpages are online.")
        logger.error(err.message)
        raise err

    for p in pages:
        _pg = BeautifulSoup(p, "html.parser")
        core = _pg.find("div", {"id": "content"})
        if not core:
            err = EmptyPageError()
            logger.error(err.message)
            continue

        # Index
        if core.select("#glossa_ordinaria"):
            yield _type_index(core)

        # Subindex
        elif core.select(".edition_intro"):
            yield _type_subindex(core)

        # Paragraph content
        elif core.select("#textContainer"):
            yield _type_paragraph(core)


def extract(*args, **kwargs) -> dict:
    """Executes the extraction of the data"""
    refs = extract_refs(*args, **kwargs)
    core = extract_raw_content(refs)
    return core