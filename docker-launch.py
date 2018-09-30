import logging

import config

from utils import optionsfile
from utils.optionsfile import OptionsFileException

from utils import commands
from utils.commands import CommandException


COMMAND_HANDLERS = {
	"container": commands.launch_container,
	"directory": commands.launch_directory
}


def map_handler(command):
	"""
	Function to map the command found to a specific handler. This allows us
	flexibility in future to add or remove commands, while keeping the code
	simple and readable.
	:paramter command: the command that was specified in the configuration file
	:retunrs: a function to call with the parameters (remaining line items)
	:       : from the configuration file.
	:       : Throws a CommandException if the command is unknown/unmapped.
	"""
	try:
		return COMMAND_HANDLERS[command]
	except KeyError:
		err_msg = f"Unimplemented command '{command}'"
		logging.error(err_msg)
		raise CommandException(err_msg)


def process_commands(commands_master_list):
	"""
	Routine to walk through all the commands imported from the configuration
	file, and invoke handlers to process the indicated work
	:param commands_master_list: a list of all the commands brought in from
	:                          : the configuration file
	:returns: Nothing
	"""
	for command_line in commands_master_list:
		temp = command_line[0]
		command = temp[0]
		params = temp[1:]

		if type(params) is not list:
			params = [params]
		try:
			handler = map_handler(command)
		except CommandException:
			logging.error("Skipping bad command, continuing processing")
			continue
		result = handler(params)
		if not result:
			logging.error(f"Error processing command '{command}' '{params}'. Continuing.")
		

def main():
	try:
		commands_list = optionsfile.read_options_file(config.CONFIG_FILE)
		process_commands(commands_list)
	except OptionsFileException as err:
		err_msg = f"Processing aborted. Options File Exception."
		err_msg = f"{err_msg} Error: {err}"
		logging.error(err_msg)
		print(err_msg)


main()