from __future__ import absolute_import
import os
import logging
import logging.config
log_file_path = open(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(log_file_path)
# Create logger
logger = logging.getLogger('subscribiecli')
from .cli import cli
