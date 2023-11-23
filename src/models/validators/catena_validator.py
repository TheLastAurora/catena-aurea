from typing import List, Dict, Union
import logging
from pprint import pprint
import os
import re
import json

# TODO: Implement all filtering and validation logic here.

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


def _by_evangelista(
    evangelium: str = None,
    exegeta: str = None,
    capitulum: int = None,
    versus: Union[int, List[int]] = None
) -> Union[List[Dict], Dict, None]:
    """
    Returns chapters information based on the specified criteria.

    Parameters:
        - evangelium (str): The name of the gospel. Use '*' for all gospels.
        - exegeta (str): The commentator.
        - capitulum (int): The chapter number.
        - versus (Union[int, List[int]]): The verse number or a list of the verses numbers.

    Returns:
        - List[Dict]: List of chapters if multiple chapters match the criteria.
        - Dict: Chapter information if a single chapter matches the criteria.
        - None: If no matching chapters are found.
    """

    if exegeta:
        if capitulum and versus:
            # Criteria: 'evangelista', 'capitulum', 'versus', 'exegeta'
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
