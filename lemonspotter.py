#!/usr/bin/env python3

'''
LemonSpotter: An incremental test suite for the MPI standard
'''

import os
import json
import argparse
import subprocess

from pathlib      import Path
from src.function import Function
from src.type     import Type
from src.constant import Constant
from src.error    import Error


def load_function(function_path):
    """
    Crawls the loaded database and searches for entry that matches name

    Paramters:
    function_path (string) : Path to the function partition of database to crawl

    Returns:
    Function: Returns an fuction object loaded with information from database
    """

    # Recursively loads all json files searching
    # for a funciton with matching name
    try:
        file = open(str(function_path))
        json_obj = json.load(file)

        # Loads all parameters from JSON
        function_name = json_obj["name"]
        return_type = json_obj["return"]
        parameters = json_obj["arguments"]
        requires = json_obj["requires"]
        start = json_obj["start"]
        end = json_obj["end"]
        return Function(function_name, return_type, parameters, requires, start, end)
    except ValueError:
        #print("Error when loading json file: " + str(path))
        pass


    return Function()

def load_type(type_path):
    """
    Crawls the loaded database and searches for entry that matches name

    Paramters:
    type_path (string) : Path to the function partition of database to crawl

    Returns:
    Type: Returns an type object loaded with information from database
    """

    # Recursively loads all json files searching
    # for a funciton with matching name
    try:
        file = open(str(type_path))
        json_obj = json.load(file)

        # Loads all parameters from JSON
        type_name = json_obj["name"]
        placeholder = json_obj["placeholder"]
        lower_range = json_obj["lower_range"]
        upper_range = json_obj["upper_range"]
        classification = json_obj["type"]
        return Type(classification, lower_range, upper_range, type_name, placeholder)
    except ValueError:
        #print("Error when loading json file: " + str(path))
        pass


    return Type()


def load_constant(constant):
    """
    Loads the constants from the database

    Paramters:
    constant (dictionary): Json based dictionary storing a single constant

    Returns a single consant object
    """
    return Constant(constant["classification"], constant["name"])


def load_error(error):
    """
    Loads the errors from the database

    Paramters:
    error (dictionary): Json based dictionary storing a single error

    Returns a single consant object
    """
    return Error(error["value"], error["symbol"])


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


def run_test(test_name, mpicc_command, max_proc_count=2, debug=False):
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
    command = mpicc_command + " " + test_name + ".c" + " -o " + test_name+"_binary"
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
        command = "mpiexec -n " + str(proc_count) + " ./" + test_name+"_binary"
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
        try:
            clean_file(test_name+"_binary")
            clean_file(test_name + ".c")
        except:
            print("Some files could not be found. Might not be deleted.")

    # Cleans stdout/stderr
    stdout = stdout.strip("\n")
    stdout = stdout.strip("\r")
    stderr = stderr.strip("\n")
    stderr = stderr.strip("\r")

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
    parser = argparse.ArgumentParser(description="Specify runtime variables", prog="LemonSpotter")

    parser.add_argument('-l', "--load",
                        metavar="db_path",
                        nargs='?',
                        const="../lemonspotter-mpi1/mpi_1_3/",
                        default="../lemonspotter-mpi1/mpi_1_3/",
                        help="specify relative path to database",
                        dest="load")

    parser.add_argument('-d', "--debug",
                        metavar="True/False",
                        nargs='?',
                        default=False,
                        help="specify true to keep generated files",
                        dest="debug")

    parser.add_argument('-m', "--mpi",
                        metavar="mpid_path",
                        nargs='?',
                        default="mpicc",
                        help="Can define a different command to compile mpi programs",
                        dest="mpi_command")

    parser.add_argument('-v', "--version",
                        help="print version of Lemonspotter",
                        action='version',
                        version="%(prog)s 0.1")

    arguments = parser.parse_args()
    if not arguments:
        parse.print_help()
        sys.exit(0)

    return arguments

def main():
    """
    Main runtime for Lemonspotter.
    """

    # There is likely a better way to parse these arguments, but it can be resolved later
    arguments = parse_arguments()

    db_path = arguments.load
    debug_state = arguments.debug
    mpi_command = arguments.mpi_command

    function_list = []
    type_list = []
    constant_list = []
    error_list = []
    element_list = []
    start_points = []
    end_points = []

    # Because functions are in different files, this must be done in a loop
    function_pathlist = Path(db_path+"functions").glob("**/*.json")
    for function in function_pathlist:
        try:
            function_list.append(load_function(function))
        except:
            pass

    # Because functions are in different files, this must be done in a loop
    type_pathlist = Path(db_path+"types").glob("**/*.json")
    for type_element in type_pathlist:
        try:
            type_list.append(load_type(type_element))
        except:
            pass

    constant_file = open(db_path+"constants.json", "r")
    json_obj = json.load(constant_file)
    for constant in json_obj:
        try:
            constant_list.append(load_constant(constant))
        except:
            pass

    error_file = open(db_path+"errors.json", "r")
    json_obj = json.load(error_file)
    for error in json_obj:
        try:
            error_list.append(load_error(error))
        except:
            pass


    for element in function_list:
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
            stdout, stderr = run_test(test_name, mpicc_command=mpi_command,debug=debug_state)

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
 
                        current_test = [start, element, end]

                        """
                        TODO: Dependencies need to be loaded here.
                              Can be done recursively from element. 
                              Iterate across all elements that the function
                              depends on. Then recursively do the same until there
                              are no more. 

                              A clean up step might be needed. Its possible that functions
                              will be duplicated. 
                        """ 


                        test_name = element.get_name()

                        generate_test(test_name + ".c", current_test)
                        stdout, stderr = run_test(test_name, mpicc_command=mpi_command, debug=debug_state)

                        if stderr == "":
                            log(test_name, "pass")
                        else:
                            log(test_name, "fail")



if __name__ == "__main__":
    main()
