from __future__ import absolute_import
import os
import logging
import logging.config
this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "logging.conf")
log_file_path = open(DATA_PATH)
logging.config.fileConfig(log_file_path)
# Create logger
logger = logging.getLogger('subscribiecli')
from .cli import cli
