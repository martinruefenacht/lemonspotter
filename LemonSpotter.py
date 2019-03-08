'''
LemonSpotter: An incremental test suite for the MPI standard
'''

import os
import json
import argparse
import subprocess
from pathlib import Path

from src.element import element



# Loads an element from JSON db
# Returns an element object populated from jsong
def load_element(db_path, name):

	# Recursively loads all json files searching
	# for a funciton with matching name
	pathlist = Path(db_path).glob("**/*.json")
	for path in pathlist:
		print(str(path))
		file = open(str(path))
		json_obj = json.load(file)

		# Loads all parameters from JSON
		element_name = json_obj["name"]

		if element_name == name:
			return_type = json_obj["return"]
			parameters = json_obj["arguments"]
			requires = json_obj["requires"]
			return element(element_name, return_type, parameters, requires)

	return element()



# Runs the paramter command passed as a string. 
# Prints what would normally be output to terminal.
# NOTE: commands must be run individually.
def run_process(command):
	command = command.split(" ");
	process = subprocess.Popen(command, cwd="tests/", stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
	stdout, stderr = process.communicate()
	print(stdout)
	print(stderr)


# Generates a test file that includes the MPI_Elements that are passed to it. 
def generate_test(file_name, elements=[]):

	# Generates test file 
	f = open("tests/" + file_name, "w+")

	# Sets up file for testing
	f.write("#include \"mpi.h\"\n")
	f.write("#include <stdio.h>\n")
	f.write("#include <stdlib.h>\n\n\n")
	f.write("int main(int argc, char** argv) {\n")

	# Writes the MPI elements to C test file
	for element in elements:
		f.write("\t"+element.text + "\n")

	f.write("return 0;\n")
	f.write("}\n")
	
	f.close()




# Cleans up test after runtime
def clean_test(file_name):
	os.remove("tests/" + file_name)


''' Testname will be the name of the test case being tested
	Testcases will be different scenarios of this testname. 
	This could be MPI_Send() with different parameter combinations.
	Results will store results of each test at its index in testcases list
'''
def log(testname, testcases = [], results=[]):

	# Open log file for specific testcase
	log_file = open("logs/" + testname + ".json", "w+")
	
	log_file.write("{\n\t\"" + testname + "\" : {\n")
	for x in range(0, len(testcases)):
		log_file.write("\t\t\"" + testcases[x] + "\" : {\n")
		log_file.write("\t\t\t\"Result\" : \"" + results[x] + "\"\n")
	
		# Tests to see if on the last element on the list	
		if (x < len(testcases)-1):
			log_file.write("\t\t}, \n")
		else:
			log_file.write("\t\t}\n")
	
	log_file.write("\t}\n")
	log_file.write("}")







# Main runtime for LemonSpotter
def main():
	test_element = load_element("../lemonspotter-mpi1/mpi_1_0/", "MPI_Init")
	print(test_element.get_arguments_list())


if __name__ == "__main__":
	main()
