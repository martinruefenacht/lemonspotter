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
                start = json_obj["start"]
                end = json_obj["end"]
                return Element(element_name, return_type, parameters, requires, start, end)
        except ValueError:
            #print("Error when loading json file: " + str(path))
            pass

    return Element()



# Runs the paramter command passed as a string.
# Prints what would normally be output to terminal.
# NOTE: commands must be run individually.
# NOTE: not currently used by lemonspotter, but is useful
#       to quickly run commands from code.
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
    return stdout, stderr

def run_test(test_name, max_proc_count=2, debug=False):
    """
    Runs the test that has been generated and has name test_name

    Paramters
    test_name      (string) : String containing the name of the test
    max_proc_count (int)    : Int containing the maximum number of times
                              run the test
    Debug          (boolaen): If debug is enabled then test files will not
                              be deleted
    """

    # Compiles test
    command = "mpicc " + test_name + ".c" + " -o " + test_name
    command = command.split(" ")
    process = subprocess.Popen(command,
                               cwd="tests/",
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True)

    stdout, stderr = process.communicate()
    if stderr != "":
        print(test_name + " : failed to compile")

    # Runs tests on as many processors as specified
    proc_count = 2
    while proc_count <= max_proc_count:
        command = "mpiexec -n " + str(proc_count) + " ./" + test_name
        command = command.split(" ")
        process = subprocess.Popen(command,
                                   cwd="tests/",
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)
        stdout, stderr = process.communicate()
        # Do Logging step here
        proc_count += 1

    # Debug can be enabled to stop from deleting
    # generated files.
    if debug is False:
        clean_file(test_name)
        clean_file(test_name + ".c")

    # Cleans stdout/stderr
    stdout = stdout.strip("\n")
    stdout = stdout.strip("\r")
    stderr = stderr.strip("\n")
    stderr = stderr.strip("\n")

    return stdout, stderr


def generate_parameters(element):
    """
    Autogenerates the text for each individual functions parameters.
    Returns a string of valid C code.

    Parameters
    element  (element)   : Gets all of the parameters needed to generate the text.
    """
    text = ""
    argument_list = element.get_arguments_list()

    for argument in argument_list:
        if argument["datatype"][:3] != "MPI":
            try:
                text += "\n\t" + argument["datatype"] + " " + argument["name"] + ";\n"
            except:
                pass

    
    return text


def generate_text(element, test_number):
    """
    Autogenerates the text for each individual function.
    Returns a string of valid C code.

    Parameters
    element  (element)   : Gets all of the parameters needed to generate the text.
    test_number (int)    : Needs a unique number so parameters are not generated redundantly

    Notes:
    Needs improvement. Current behavior is to interpret all MPI defined elements as MPI_COMM_WORLD
    Also could potentially try to generate more than one element of the same type. Needs to be iterative.
    """
    text = ""
    argument_list = element.get_arguments_list()

    #Generates parameters
    for argument in argument_list:
        text += "\t"+ argument["datatype"] + " "
        if argument["pointer"] != 0:
            for _ in range(0, argument["pointer"]-1):
                text += "*"
        text += argument["name"] + str(test_number) + ";\n"


    # Generates function call
    text += "\t"+ element.get_name() + "("
    for argument in argument_list:
        try:
            if argument["pointer"] != 0:
                text += "&"
        except:
            pass
        if argument["datatype"][:3] != "MPI":
            text += argument["name"] + str(test_number) + ", "
        else:
            text += "MPI_COMM_WORLD, "

    # Removes extra comma that gets appended at the end
    if len(argument_list) != 0:
        text = text[0:len(text)-2]
    text += ");"
    return text




def generate_test(file_name, elements=[]):
    """
    Autogenerates the C test files for each test.

    Parameters:
    file_name (string)   : Name of the file that will be created
    elements  (string[]) : List of strings cooresponding to the elements to be included in test
    """

    # To be used in paramter names to avoid conflicts
    test_number = 0

    # Generates test file
    file = open("tests/" + file_name, "w+")

    # Sets up file for testing
    file.write("#include \"mpi.h\"\n")
    file.write("#include <stdio.h>\n")
    file.write("#include <stdlib.h>\n\n\n")
    file.write("int main() {\n")

    # Writes the MPI elements to C test file
    for element in elements:
        file.write(generate_text(element, test_number) + "\n\n")



    file.write("\treturn 0;\n")
    file.write("}\n")
    file.close()


def clean_file(file_name):
    """
    Deletes the associated file_name from tests directory.

    Paramters:
    file_name (string) : The name of the file being deleted
    """
    os.remove("tests/" + file_name)



def log(testname, results):
    """
    Logs output of all testcases for a specific test to a log file.
    """

    # Open log file for specific testcase
    log_file = open("logs/" + testname + ".json", "w+")

    log_file.write("{\n\t\"" + testname + "\" : {\n")
    log_file.write("\t\t\"status\" : " + "\"" + results + "\"\n")

    log_file.write("\t}\n")
    log_file.write("}")


def parse_arguments():
    """
    Parses arguments from the command line launch command. Returns path to library
    database
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

    parser.add_argument('-d', "--debug",
                        metavar="True/False",
                        nargs='?',
                        default=False,
                        help="specify true to keep generated files",
                        dest="debug")

    parser.add_argument('-v', "--version",
                        help="print version of Lemonspotter",
                        action='version',
                        version="%(prog)s 0.1")

    return parser.parse_args()


def main():
    """
    Main runtime for Lemonspotter.
    """

    # There is likely a better way to parse these arguments, but it can be resolved later
    db_path = parse_arguments().load

    debug_state = parse_arguments().debug

    full_list = []
    element_list = []
    start_points = []
    end_points = []

    pathlist = Path(db_path).glob("**/*.json")
    for path in pathlist:
        try:
            file = open(str(path))
            json_obj = json.load(file)
            full_list.append(load_element(db_path, json_obj["name"]))
        except:
            pass

    for element in full_list:
        if element.get_start() == True:
            start_points.append(element)
        elif element.get_end() == True:
            end_points.append(element)
        else:
            element_list.append(element)

    # Ensures that all endpoints work. 
    for start in start_points:
        for end in end_points:
            endpoint_list = [start, end]
            test_name = start.get_name() + "__" + end.get_name()
            generate_test(test_name + ".c", endpoint_list)
            stdout, stderr = run_test(test_name, debug=debug_state)

            if stderr == "":
                start.set_validation(True)
                end.set_validation(True)
                log(start.get_name(), "pass")
                log(end.get_name(), "pass")
            else:
                start.set_validation(False)
                end.set_validation(False)
                log(start.get_name(), "fail")
                log(end.get_name(), "fail")


    # Runs tests of all functions through all start/end points
    for start in start_points:
        # Ensures that this start point is tested and valid
        if start.get_validation():
            
            for end in end_points:
                # Ensures that this endpoint is tested and valid
                if end.get_validation():

                    for element in element_list:   
                        current_test = [start, element ,end]
                        test_name = element.get_name()

                        generate_test(test_name + ".c", current_test)
                        stdout, stderr = run_test(test_name, debug=debug_state)

                        if stderr == "":
                            log(test_name, "pass")
                        else:
                            log(test_name, "fail")



if __name__ == "__main__":
    main()
