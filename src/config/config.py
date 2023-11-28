import logging.config
import yaml
import os


with open(os.path.join('./config', 'settings.yaml'), 'r') as f:
    conf = yaml.safe_load(f.read())


def get_logger(name: str) -> logging.Logger:
    logs_dir = conf['logging']['root_path']
    os.makedirs(logs_dir, exist_ok=True)
    logging.config.dictConfig(conf['logging'])
    return logging.getLogger(name)


def get_out(name: str) -> (str, str):
    out_dir = conf['output']['root_path']
    os.makedirs(out_dir, exist_ok=True)
    return conf['output']['sources'][name]['filename'], conf['output']['sources'][name]['encoding']


def get_input(name: str) -> (str, str):
    input_file = conf['input'][name]
    if not os.path.exists(input_file['path']):
        raise FileNotFoundError("No files input files provided.")
    return input_file['path'], input_file['encoding']


def get_crawler_url() -> str:
    return conf['services']['crawler']['url']
