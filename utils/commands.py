import logging
import os
import subprocess
import yaml


class CommandException(Exception):
	"""
	Base exception for this module. Used to help indicate where an
	exception came from (i.e. this module versus another module).
	"""
	pass


def exec_cmd_with_output(command):
	"""
	Utility function to execute a command and capture output and return code
	:param command: type list. [0] is the command, [1] and on are params for
	:             : the command. i.e. [ "find", ".", "-print"]
	:returns first: the return code from executing the command
	:       second: string of the output captured from the command
	"""
	result = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE)
	retcode = result.returncode
	output = result.stdout.decode('utf-8')
	return retcode, output


def container_image_exists(container_name):
	"""
	Utility funciton to validate that a container exists in the docker images
	repository. If bad return code (this indicates a more serious issue than
	just the container image does not exist) or empty input come back from the 
	docker command, then we indicate the container does not exist. Otherwise,
	the output would be the container ID of the specified container.
	:param container_name: the name of the container to check for in the
	:                    : docker images repository
	:return: True if the container exists, otherwise False
	"""
	command = ["docker", "images", "-q", container_name]
	status, output = exec_cmd_with_output(command)
	if status != 0 or len(output) == 0:
		return False
	else:
		return True

		
def is_yaml(container_name):
	"""
	Utility to test if the container name specified is a valid Yaml file.
	:param container_name: the container name/file name we want to test
	:returns: True if valid Yaml file, otherwise False
	"""
	# if the container is not a file, then it cannot be a docker-compose
	# YAML file
	if not file_exists(container_name):
		return False
	try:
		with open(container_name, "r") as stream:
			temp = yaml.load(stream)
			if temp is None:
				return False
	except yaml.YAMLerror:
		return False
	return True
		

def file_exists(filename):
	"""
	Utility function to check if a specified file exists (or not)
	:param filename: the file name to validate exists
	:returns: True if the file exists and is a file (e.g. not a directory),
	:         otherwise False.
	"""
	return os.path.isfile(filename)


def directory_exists(directory):
	"""
	Utility function to check if a specified directory exists (or not)
	:param directory: the directory name or path to validate exists
	:returns: True if the directory exists and is a directory (e.g. not a
	:         file), otherwise False.
	"""
	return os.path.isdir(directory)


def launch_container(command_args, directory=None):
	"""
	Handles all the logic around launching a single container. Includes
	validating that the image exists, and various invocation methods.
	:param command_args: the list containing the command line (all elements)
	:                  : that came from the configuration file. All elements
	:                  : in the list are arguments for this command.
	:returns: True if successful, otherwise False
	"""
	container = command_args[0]
	if directory is not None:
		full_container = f"{directory}/{container}"
	else:
		full_container = container
	# yaml must have full path specified.
	if is_yaml(full_container):
		command = ["docker-compose", "-f", full_container, "up", "-d"]	
	else:
		exists = container_image_exists(container)
		if not exists:
			logging.error(f"Container image '{container}' does not exist. Not launched.")
			return False
		command = ["docker", "run", "-d", container]

	status, output = exec_cmd_with_output(command)
	
	if status == 0:
		return True
	
	return False
	
	
def launch_directory(command_args):
	"""
	Performs a walk through the specified directory, and attempts to launch
	all containers (all filenames specified in the directory). Uses the
	launch_container on each one, so we inherit all the validation and
	execution logic we already worked on for individual containers.
	:param command_args: the list containing the command line (all elements)
	:                  : that came from the configuration file. All elements
	:                  : in the list are arguments for this command.
	:returns: True if all containers launched successfully, otherwise False
	"""
	dir = command_args[0]
	dir = dir.rstrip('/')
	if not directory_exists(dir):
		logging.error(f"Directory '{dir}' does not exist or is not a directory.")
		return False
		
	all_success = True
	for dirName, subdirList, filelist in os.walk(dir):
		for fname in filelist:
			result = launch_container([fname], directory=dir)
			all_success = all_success and result
		# erase all subdirs. we only want to traverse the files in the
		# current directory
		del subdirList[:]
	return all_success
	