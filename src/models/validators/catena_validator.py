import logging
import os
import bs4
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

def _load_schema():
    schema = {}
    with open(
        os.path.join(os.path.dirname(__file__), "../schemas/catena_schema.json")
    ) as f:
        schema = json.load(f)
    
