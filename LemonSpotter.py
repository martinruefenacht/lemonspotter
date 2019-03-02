'''
LemonSpotter: An incremental test suite for the MPI standard
'''

import os
import argparse
import subprocess


def main():
	generate_test("test.c")
	run_process("mpicc test.c -o test")
	run_process("mpiexec -n 4 ./test")
	clean_test("test.c")
	clean_test("test")



# Runs the paramter command passed as a string. 
# Prints what would normally be output to terminal.
# NOTE: commands must be run individually.
def run_process(command):
	command = command.split(" ");
	process = subprocess.Popen(command, cwd="tests/", stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
	stdout, stderr = process.communicate()
	print(stdout)


# Generates a test file that includes the MPI_Elements that are passed to it. 
def generate_test(file_name, MPI_Elements=[]):
	
	# Generates test file 
	f = open("tests/" + file_name, "w+")

	# Sets up file for testing
	f.write("#include \"mpi.h\"\n")
	f.write("#include <stdio.h>\n")
	f.write("#include <stdlib.h>\n\n\n")
	f.write("int main(int argc, char** argv) {\n")

	# Writes the MPI elements to C test file
	for element in MPI_Elements:
		f.write(element.text + "\n")

	f.write("return 0;\n")
	f.write("}\n")
	
	f.close()



# Cleans up test after runtime
def clean_test(file_name):
	os.remove("tests/" + file_name)


if __name__ == "__main__":
	main()