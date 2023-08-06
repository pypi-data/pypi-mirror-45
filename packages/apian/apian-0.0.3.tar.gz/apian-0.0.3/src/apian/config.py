"""
Read configuration from a location determined by the library.
"""
import logging
import logging.config
import os
from functools import lru_cache

import miniscule
import yaml

log = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def read_config():
    """Uses the miniscule library to read configuration at the path specified by
    `CONFIG` environment variable.
    """
    path = os.environ.get('CONFIG', 'config.yaml')
    try:
        config = miniscule.read_config(path)
        config['__path'] = path
        return config
    except FileNotFoundError:
        print("No file at", path)
        return None


def init_logging(path):
    # Let the application take care of logging
    logging.getLogger('werkzeug').handlers = []
    if path is None:
        return

    with open(path, 'r') as handle:
        log_config = yaml.load(handle.read(), Loader=yaml.SafeLoader)
        logging.config.dictConfig(log_config)
