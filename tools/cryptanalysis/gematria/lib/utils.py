"""
    Utility functions for Gematria
"""

from __future__ import annotations
from math import sqrt
import os
import logging, coloredlogs
logger = logging.getLogger(__name__)

def hamming_distance(string1: str, string2: str) -> int:
	"""Calculates Hamming Distance between 2 strings"""
	if len(string1) != len(string2):
		logger.critical(f"[HAMMING DISTANCE] STRINGS MUST BE OF EQUAL LENGTH;\n1.{string1}\n2.{string2}")
		return 128

	if len(string1) != 128:
		logger.critical(f"[HAMMING DISTANCE] STRINGS ARE NOT 64 BIT DIGESTED;\n1.{string1}\n2.{string2}")
		return 128

	distance: int = 0
	for char1, char2 in zip(string1, string2):
		if char1 != char2:
			distance += 1

	return distance

def file_into_array(file_path: str) -> List:
	"""Read file contents into an array seperating by EOL"""
	content = []
    
	# Read content
	with open(file_path) as f:
		content = f.readlines()
    
	# Remove "\n" from content
	formated_content = [c[:-1] for c in content]

	return formated_content

def get_file_name(file_path: str) -> str:
	"""Strip full path and file extensions from full_path str"""
	sp = file_path.split("/")
	return sp[len(sp) - 1][:-4]

def reverse_int(num: int) -> int:
	"""Reverse int"""
	assert isinstance(num, int)

	reversed_num = 0

	# start a while loop till complete number has been reversed
	while num != 0 :

		# taking modulo with 10 gives us the last digit of num
		curr_digit = num % 10

		# appending the last digit of num to reversed_num
		# for this we multiply the curr reversed_num by 10 and add curr_digit to it
		reversed_num = 10*reversed_num 
		reversed_num = reversed_num + curr_digit
    
		# remove the last digit from num by dividing it by 10
		num = num // 10
    
	# we get the reversed_num
	return reversed_num

def is_prime(num: int) -> bool:
	"""is a number prime"""
	assert isinstance(num, int)

	# this flag maintains status whether the n is prime or not
	prime_flag = 0
 
	if num > 1:
		# Check if number is divisible through ---
		for i in range(2, int(sqrt(num)) + 1):
			if (num % i == 0):
				prime_flag = 1
				break

		# Check if it was divisible, 0 if it wasnt
		if prime_flag == 0:
			return True
		return False

	return False

def get_prime_and_emirp(number: int) -> tuple:
	"""Get's the result of prime and emirp of a number"""
	# Number Prime
	number_prime = is_prime(number)
	
	# Number Emirp
	number_emirp = is_prime(reverse_int(number))
	
	return (number_prime, number_emirp)
