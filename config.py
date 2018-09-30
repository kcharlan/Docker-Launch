import sys
import os
import logging

logging.basicConfig(level=logging.INFO)

#INSTALLED_PATH = '/usr/local/sbin/docker-launch'
INSTALLED_PATH = '/Users/kevinharlan/Documents/Development/Docker-Launch'

try:
	sys.path.index(INSTALLED_PATH)
except ValueError:
	sys.path.append(INSTALLED_PATH)


#CONFIG_FILE = '/etc/docker-launch.conf'
CONFIG_FILE = f'{INSTALLED_PATH}/samples/sample-docker-launch.conf'
