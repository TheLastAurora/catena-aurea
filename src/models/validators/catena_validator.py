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

def _request_data():
    """Gets the data for the given pattern"""
    pass
 
def _filter_data():
    """Checks whether the data exists or not, filtering based on the type of search
    
        evangelist -> returns all chapters;
        evangelist, chapter -> returns all verses from the chapter;
        evangelist, chapter, verse -> returns all comments for the given verse;
        evangelist, commentator -> returns all comments of any evangelist given the commentator;
        commentator -> returns all comments from this commentator.
    """
    pass
