'''
LemonSpotter: An incremental test suite for the MPI standard
'''

import os
import json
import argparse
import subprocess

from pathlib import Path
from src.element import Element


def load_element(db_path, name):
    """
    Crawls the loaded database and searches for entry that matches name

    Paramters:
    db_path (string) : Path to the database to crawl
    name    (string) : Name of the element to be loaded

    Returns:
    element: Returns an element loaded with information from database
    """

	# Recursively loads all json files searching
	# for a funciton with matching name
    pathlist = Path(db_path).glob("**/*.json")
    for path in pathlist:
        try:
            file = open(str(path))
            json_obj = json.load(file)

            # Loads all parameters from JSON
            element_name = json_obj["name"]

            if element_name == name:
                return_type = json_obj["return"]
                parameters = json_obj["arguments"]
                requires = json_obj["requires"]
                return Element(element_name, return_type, parameters, requires)
        except ValueError:
            print("Error when loading json file: " + str(path))

    return Element()



# Runs the paramter command passed as a string.
# Prints what would normally be output to terminal.
# NOTE: commands must be run individually.
def run_process(command):
    """
    Runs a CLI process; used for running C test files.

    Paramters:
    command (string) : Command is the command that will be run
    """
    command = command.split(" ")
    process = subprocess.Popen(command,
                               cwd="tests/",
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True)

    stdout, stderr = process.communicate()
    print(stdout)
    print(stderr)


def generate_test(file_name, elements=[]):
    """
    Autogenerates the C test files for each test.

    Parameters:
    file_name (string)   : Name of the file that will be created
    elements  (string[]) : List of strings cooresponding to the elements to be included in test
    """

    print(elements)

    # Generates test file
    file = open("tests/" + file_name, "w+")

    # Sets up file for testing
    file.write("#include \"mpi.h\"\n")
    file.write("#include <stdio.h>\n")
    file.write("#include <stdlib.h>\n\n\n")
    file.write("int main(int argc, char** argv) {\n")

    # Writes the MPI elements to C test file


    file.write("return 0;\n")
    file.write("}\n")
    file.close()





def clean_test(file_name):
    """
    Deletes the associated file_name from tests directory.

    Paramters:
    file_name (string) : The name of the file being deleted
    """
    os.remove("tests/" + file_name)



def log(testname, testcases=[], results=[]):
    """
    Logs output of all testcases for a specific test to a log file.

    Parameters:
    testname (string)   : String of type of test being run
    tescases (string[]) : List of strings cooresponding to individual testcases
    results  (string[]) : List of integers cooresponding to the results the testcases
    """

    # Open log file for specific testcase
    log_file = open("logs/" + testname + ".json", "w+")

    log_file.write("{\n\t\"" + testname + "\" : {\n")
    for case, index in enumerate(testcases, 0):
        log_file.write("\t\t\"" + case + "\" : {\n")
        log_file.write("\t\t\t\"Result\" : \"" + results[index] + "\"\n")

        # Tests to see if on the last element on the list
        if index < len(testcases)-1:
            log_file.write("\t\t}, \n")
        else:
            log_file.write("\t\t}\n")

    log_file.write("\t}\n")
    log_file.write("}")


def main():
    """
    Main runtime for Lemonspotter.
    """

    # Parse CLI Arguments for more granular control
    parser = argparse.ArgumentParser(description="Specify runtime variables", prog="Lemonspotter")

    parser.add_argument('-l', "--load",
                        metavar="db_path",
                        nargs='?',
                        const="../lemonspotter-mpi1/mpi_1_0/",
                        default="../lemonspotter-mpi1/mpi_1_0/",
                        help="specify relative path to database",
                        dest="load")

    parser.add_argument('-v', "--version",
                        help="print version of Lemonspotter",
                        action='version',
                        version="%(prog)s 0.1")

    db_path = parser.parse_args().load

    test_element = load_element(db_path, "MPI_Init")
    print(test_element.get_arguments_list())


if __name__ == "__main__":
    main()
