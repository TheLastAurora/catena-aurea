from typing import Dict, List
from models.extract import extract
from config.config import get_logger, get_input
from pprint import pprint
import os
import re
import json

# TODO: Implement html formating and validation.


# Please, reference the crawler output for the specific interval of the Catena index.
INTERVAL_LOC = ['"A propos de cette \u00e9dition?&"', 'Table des mati']
logger = get_logger('catena_validator')

# Loading schema
global schema
global data

filename, encoding = get_input('catena')
with open(file=filename, encoding=encoding, mode='r') as f:
    schema = json.load(f)


def _by_evangelista(evangelium: str = '*', exegeta: str = None, capitulum: int = None, versus: int | list[int] = None) -> list[dict] | dict | None:
    if exegeta:
        if capitulum and versus:
            # Criteria: 'evangelista', 'capitulum', 'versus', 'exegeta'
            content = extract(interval=INTERVAL_LOC)
            pass
        else:
            # Criteria: 'evangelista', 'exegeta'
            pass
    else:
        if capitulum and versus:
            # Criteria: 'evangelista', 'capitulum', 'versus'
            pass
        else:
            # Criteria: 'evangelista'
            if evangelium == '*':
                # All gospels
                pass
            else:
                # Only selected gospel
                pass
    # Placeholder return
    return None


def _by_commentator(exegeta: str) -> List[Dict]:
    """
    Retrieves chapter information for a given commentator.

    Parameters:
        - exegeta (str): The commentator.

    Returns:
        - List[Dict]: List of chapter information for the specified commentator.
    """

    # Using _by_evangelista to get all data and then filter
    evangeliums = [_by_evangelista(exegeta)]

    # Placeholder return
    return evangeliums
