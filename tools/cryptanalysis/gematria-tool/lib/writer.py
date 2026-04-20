"""
    Class that handles file writting
"""

import os
from datetime import datetime

class Writer:
	"""
		Writer class for file handling and writting
		It will write to a file with the name of the message being
		analysed, ex: 'The Instar Emergence.txt'
	"""

	# File to write to
	file_path: str

	# Directory where files are stored
	directory_path: str

	# Full pat (directory_path + / + file_path)
	full_path: str

	def __init__(self, message:str) -> None:
		self.directory_path = "outputs/"
		self.file_path = f"{message}.txt"
		self.full_path = os.path.join(self.directory_path, self.file_path)

		if not self.directory_exists():
			os.makedirs(self.directory_path)

		# if already exists clear contents
		with open(self.full_path, 'w', encoding='UTF-8') as file_obj:
			file_obj.write(f"COMPUTING \"{message}\" STARTED AT {str(datetime.now())}\n")
			# self.divisor(file_obj)

	def write(self, string: str, print_time: bool = True) -> None:
		"""Writes into file"""
		with open(self.full_path, 'a', encoding='UTF-8') as file_obj:
			if print_time:
				file_obj.write(f"{string} >>> {str(datetime.now())}\n")
			else:
				file_obj.write(f"{string}\n")

	def divisor(self, file_obj) -> None:
		"""Puts divisor in a file obj"""
		file_obj.write("-" * 252 + "\n")

	def title(self, string:str) -> None:
		"""Prints tilte-like string in txt file"""
		with open(self.full_path, 'a', encoding='UTF-8') as file_obj:
			self.divisor(file_obj)
			file_obj.write(f"   {string} >>> {str(datetime.now())}\n")
			self.divisor(file_obj)

	def chapter(self, string:str) -> str:
		"""Prints chapter-like string in file obj"""
		output_str = f"{string}\n"
		output_str += "-" * (len(string) + 4)

		with open(self.full_path, 'a', encoding='UTF-8') as file_obj:
			file_obj.write(output_str)

		return output_str

	def write_and_print(self, string:str, print_time:bool = True) -> None:
		"""Helper function to write into file and cmd"""
		self.write(string, print_time)
		print(string)

	def directory_exists(self) -> bool:
		"""Checks if output files directory exists"""
		return os.path.exists(self.directory_path)

	def file_exists(self) -> bool:
		"""Checks if file already exists"""
		return os.path.exists(self.full_path)
