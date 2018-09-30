import logging

class OptionsFileException(Exception):
	"""
	Base exception for this module. Used to help indicate where an
	exception came from (i.e. this module versus another module).
	"""
	pass


def read_options_file(filename):
	"""
	Utility to parse the options file, in preparation for acting on the
	commands contained within it.
	:param filename: the name of the configuration options file to read, which
	:              : can include a path
	:return: A list of lists. Each list entry is a list of the tokens found
	:      : on that line.
	:      : [  [ "directory", "/a/b/c"], ["container", "my-image"] ]
	"""
	master_list = []
	try:
		with open(filename) as f:
			for line in f:
				result = process_line(line)
				if result is None:
					continue
				master_list.append(result)
		return master_list
	except OSError as err:
		logging.error(f"OS error accessing file {filename}: {err}")
		raise OptionsFileException(err, f"Unable to access config file {filename}")
	except FileNotFoundError:
		err_msg = f"File {filename} not found."
		logging.error(err_msg)
		raise OptionsFileException(err_msg)
		
		
def process_line(data):
	"""
	Processor to parse each individual config file line
	:param data: the line read from the file
	:returns: None if it is a line we don't wish to handle, otherwise
	:       : a list containing each individual token.
	"""
	command_list = []
	temp = data.strip()
	if len(temp) == 0:
		return None
	if temp[0] == '#':
		return None
	temp2 = temp.split()
	command_list.append(temp2)
		
	return command_list
