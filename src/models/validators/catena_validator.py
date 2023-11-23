import logging
from pprint import pprint
import os
import re
import json

# TODO: Define classes to be used for Catena - implement all logic here.

log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, "catena.log"),
    format="%(asctime)s %(message)s",
    level=logging.ERROR,
    filemode="w",
)

# Loading schema
global schema
global data

with open(os.path.join(os.path.dirname(__file__), "../schemas/catena_schema.json")) as f:
    schema = json.load(f)


def _by_evangelista(evangelium: str) -> list[dict]:
    """Returns all the chapters from evangelium"""
    # THIS IS THE STARTPOINT 1
    pass

def _by_commentator(exegeta: str) -> list[dict]:
    """Returns all comments made by the exegeta"""
    # THIS IS THE STARTPOINT 2
    pass

def _by_chapter(gospel: list) -> list[dict]:
    """Filters all gospels per chapter"""
    pass

def _by_verse(chapter: list) -> list[dict] | dict:
    """Filters all chapters from gospel per verse (or verses)"""
    pass


def extract_data(*args, **kwargs) -> dict:
    """Establishes an interface for extracting the data"""

    # User input, thats why is in latin, not english.

    _args = frozenset([kwarg for kwarg in kwargs.keys() if kwarg])
    # Defining execution flow (filtering)
    func_mapping = {
        frozenset(['exegeta']): _by_commentator(),
        frozenset(['evangelista']): _by_evangelista(),
        frozenset(['evangelista', 'exegeta']): _by_evangelista(_by_commentator()),
        frozenset(['evangelista', 'capitulum']): _by_chapter(_by_evangelista()),
        frozenset(['evangelista', 'capitulum', 'versus']): _by_verse(_by_chapter(_by_evangelista())),
        frozenset(['evangelista', 'capitulum', 'versus', 'exegeta']): _by_verse(_by_chapter(_by_evangelista(_by_commentator())))
    }

    # It probably doesn't work yet, this is just to remember the concept.
    res = func_mapping[_args](args, **kwargs)
    return res



