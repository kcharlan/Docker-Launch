import logging
import os
import shutil

import config
from utils.commands import directory_exists, file_exists


CURRENT_DIR = config.SOURCE_PATH


def copy_install_files():
	"""
	Copies all files from the current directory tree, current folder and all
	subfolders (which should be the directory all the docker-launch routines
	reside in) to the INSTALLED_PATH.
	: params none:
	: return: nothing. Will raise an Exception if errors are encountered.
	"""
	print("\nCopying over install files.")
	dest_dir = config.INSTALLED_PATH
	if directory_exists(dest_dir):
		err_msg = f"Destination directory '{dest_dir}' already exists. Aborting install."
		logging.critical(err_msg)
		raise Exception(err_msg)
	try:
		shutil.copytree(CURRENT_DIR, dest_dir)
		print(f"\tdocker-launch files now installed in {dest_dir}\n")
	except (IOError, os.error) as why:
		err_msg = f"Install directory copy failed: {why}.\nAborting install."
		logging.critical(err_msg)
		raise Exception(err_msg)

		
def copy_file(source_file, dest_file):
	"""
	General purpose file copy routine, since we are doing a couple of them
	explicitly.
	: params source_file: the file to copy from
	: params dest_file: the file to copy to
	: return: nothing. Will raise an Exception if errors are encountered.
	"""
	if file_exists(dest_file):
		err_msg = f"File target already exists: '{dest_file}'\n"
		err_msg = f"{err_msg}Aborting install."
		logging.critical(err_msg)
		raise Exception(err_msg)
	
	try:
		shutil.copyfile(source_file, dest_file)
	except (IOError, os.error) as why:
		err_msg = f"File copy failed: {why}. Aborting install."
		logging.critical(err_msg)
		raise Exception(err_msg)


def copy_config_file():
	"""
	Copies the configuration file to its proper path name and destination
	config.CONFIG_FILE.
	: params none:
	: return: nothing. Will raise an Exception if errors are encountered.
	"""
	print("Copying over configuration file.")
	source_file = f"{CURRENT_DIR}/samples/sample-docker-launch.conf"
	dest_file = config.CONFIG_FILE
	try:
		copy_file(source_file, dest_file)
		print(f"\tConfig file {dest_file} now in place.\n")
	except:
		err_msg = "Configuration file copy failed."
		logging.critical(err_msg)
		raise


def copy_initd_file():
	"""
	Copies the init.d script file to its proper path name and destination
	/etc/init.d/docker-launch.sh
	: params none:
	: return: nothing. Will raise an Exception if errors are encountered.
	"""
	print("Copying over init.d file.")
	source_file = f"{CURRENT_DIR}/samples/docker-launch.sh"
	dest_file = f"{config.INIT_PATH}/docker-launch.sh"
	try:
		copy_file(source_file, dest_file)
		print(f"\tInit file {dest_file} now in place.\n")
	except:
		err_msg = "Init.d file copy failed."
		logging.critical(err_msg)
		raise


def install():
	"""
	Performs the installation workflow.
	: params none:
	: return: nothing. Will raise an Exception if errors are encountered.
	"""
	try:
		copy_install_files()
		copy_config_file()
		copy_initd_file()
		print("\n\nInstall completed successfully.\n")
		print("Proceed with final install steps and modifications to the configuration files and scripts.\n\n")
	except Exception as err:
		logging.critical("Installation failed. See error messages for details.")


install()
