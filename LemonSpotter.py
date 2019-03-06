'''
LemonSpotter: An incremental test suite for the MPI standard
'''

import os
import json
import argparse
import subprocess

from src.element import element



# Loads an element from JSON db
# Returns an element object populated from json
def load_element(file_path):
	file = open(file_path)
	json_obj = json.load(file)

	name = json_obj["name"]
	text = json_obj["text"]
	dependencies = json_obj["dependencies"]

	return element(name, text, dependencies)



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



# Main runtime for LemonSpotter
def main():

	'''
	init = element("MPI_Init()", "\tMPI_Init(&argc, &argv);\n")
	finalize = element("MPI_Finalize", "\tMPI_Finalize();\n")
	elements = [init, finalize] 
	generate_test("test.c", elements)
	run_process("mpicc test.c -o test")
	run_process("mpiexec -n 4 ./test")
	clean_test("test.c")
	clean_test("test")
	'''





if __name__ == "__main__":
	main()
