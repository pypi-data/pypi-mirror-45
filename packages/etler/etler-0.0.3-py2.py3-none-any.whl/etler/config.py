import os
from pathlib import Path

import yaml

ROOT = Path(__file__).parent
CONFIG_PATH = os.path.join(ROOT, "settings.yml")

with open(CONFIG_PATH, 'r') as config_file:
    config = yaml.safe_load(config_file)


def fetch(attribute):
    return config[attribute]
