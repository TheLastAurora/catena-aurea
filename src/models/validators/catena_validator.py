import logging
import os 
import bs4
import re
import json

# TODO: Define classes to be used for Catena (implement all logic here).

# logging.basicConfig(filename=os.path.join(log_dir, 'catena_validator.log'), format='%(asctime)s %(message)s', level=logging.ERROR, filemode='w')

if __name__ == '__main__':
    schema = {}
    with open(os.path.join(os.path.dirname(__file__), '../schemas/catena_schema.json')) as f:
        schema = json.load(f)
    pass