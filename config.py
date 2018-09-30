import sys
import os
import logging

logging.basicConfig(level=logging.INFO)

# need to hard set our source path, so we can import modules from subfolders
module_file = sys.modules[__name__].__file__
SOURCE_PATH = os.path.dirname(module_file)

try:
	sys.path.index(SOURCE_PATH)
except ValueError:
	sys.path.append(SOURCE_PATH)

CONFIG_FILE = '/etc/docker-launch.conf'

INIT_PATH = '/etc/init.d'

INSTALLED_PATH = '/usr/local/sbin/docker-launch'
