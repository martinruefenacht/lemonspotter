#!/usr/bin/env python3

'''
LemonSpotter: An incremental test suite for the MPI standard
'''

import sys
import os
import json
import argparse
import subprocess
import pathlib
import logging

from src.function import Function
from src.type     import Type
from src.constant import Constant
from src.error    import Error

def load_function(defaults, function_path):
    """
    Crawls the loaded database and searches for entry that matches name

    Paramters:
    function_path (string) : Path to the function partition of database to crawl

    Returns:
    Function: Returns an fuction object loaded with information from database
    """

    with open(function_path, 'r') as function_file:
        json_obj = json.load(function_file)

        # required function attributes
        function_name = json_obj["name"]
        logging.info("function loading: %s", function_name)

        return_type = json_obj["return"]
        version = json_obj["version"]

        parameters = json_obj.get("parameters", defaults['function']['parameters'])
        
        # for each parameter
        for parameter in parameters:
            # complete parameter definition from default
            if 'pointer' not in parameter:
                parameter['pointer'] = defaults['parameter']['pointer']

            if 'const' not in parameter:
                parameter['const'] = defaults['parameter']['const']

            if 'direction' not in parameter:
                parameter['direction'] = defaults['parameter']['direction']

        needs_any = json_obj.get('needs_any', defaults['function']['needs_any'])
        needs_all = json_obj.get('needs_all', defaults['function']['needs_all'])

        leads_any = json_obj.get('leads_any', defaults['function']['leads_any'])
        leads_all = json_obj.get('leads_all', defaults['function']['leads_all'])

        return Function(function_name, return_type, parameters, needs_any, needs_all, leads_any, leads_all)

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
        type_file = open(str(type_path))
        json_obj = json.load(type_file)

        # Loads all parameters from JSON
        type_name = json_obj["name"]
        placeholder = json_obj["placeholder"]
        lower_range = json_obj["lower_range"]
        upper_range = json_obj["upper_range"]
        classification = json_obj["type"]
        return Type(classification, lower_range, upper_range, type_name, placeholder)

    except ValueError:
        logging.error("Failed to load %s.", path)

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

# Runs the parameter command passed as a string.
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

    if stderr:
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
    if not debug:
        try:
            clean_file(test_name+"_binary")
            clean_file(test_name + ".c")

        except OSError:
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
    Also could potentially try to generate more than one element of the same type.
    Needs to be iterative.
    """
    text = ""
    argument_list = element.parameters

    #Generates parameters
    for argument in argument_list:
        text += "\t"+ argument["datatype"] + " "
        if argument["pointer"] != 0:
            for _ in range(0, argument["pointer"]-1):
                text += "*"
        text += argument["name"] + str(test_number) + ";\n"


    # Generates function call
    text += "\t"+ element.function_name + "("
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
    if argument_list:
        text = text[0:len(text)-2]
    text += ");"
    return text

def generate_test(file_name, elements=None):
    """
    Autogenerates the C test files for each test.

    Parameters:
    file_name (string)   : Name of the file that will be created
    elements  (string[]) : List of strings cooresponding to the elements to be included in test
    """

    # create tests directory
    if not os.path.isdir("tests"):
        os.mkdir("tests")

    # To be used in paramter names to avoid conflicts
    test_number = 0

    # Generates test file
    test_file = open("tests/" + file_name, "w+")

    # Sets up file for testing
    test_file.write("#include \"mpi.h\"\n")
    test_file.write("#include <stdio.h>\n")
    test_file.write("#include <stdlib.h>\n\n\n")
    test_file.write("int main() {\n")

    # Writes the MPI elements to C test file
    for element in elements:
        test_file.write(generate_text(element, test_number) + "\n\n")

    test_file.write("\treturn 0;\n")
    test_file.write("}\n")
    test_file.close()

def clean_file(file_name):
    """
    Deletes the associated file_name from tests directory.

    Paramters:
    file_name (string) : The name of the file being deleted
    """
    os.remove("tests/" + file_name)

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
                        action='store_true',
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

    parser.add_argument('--log',
                        default="warning")

    arguments = parser.parse_args()

    # check that arguments were given
    if not arguments:
        parser.print_help()
        sys.exit(0)

    return arguments

def parse_functions(default_path, path):
    """
    Parse all functions in the path given.
    """

    functions = []

    # parse fault function
    with open(default_path) as default_file:
        defaults = json.load(default_file)
    
        function_pathlist = pathlib.Path(path).glob("**/*.json")

        for function_path in function_pathlist:
            func = load_function(defaults, function_path)
            if func:
                functions.append(func)
    
    return functions

def parse_types(path):
    """
    Parse all types given by the path.
    """

    type_list = []

    type_pathlist = pathlib.Path(path).glob("**/*.json")

    for type_element in type_pathlist:
        try:
            type_list.append(load_type(type_element))
        except:
            pass

    return type_list

def parse_constants(path):
    """
    Parse all constants from file path given.
    """

    constant_list = []
    constant_file = open(path, "r")

    json_obj = json.load(constant_file)
    for constant in json_obj:
        try:
            constant_list.append(load_constant(constant))
        except:
            pass

    return constant_list

def parse_errors(path):
    """
    Parse all errors from file path given.
    """

    error_list = []
    error_file = open(path, "r")
    json_obj = json.load(error_file)
    for error in json_obj:
        try:
            error_list.append(load_error(error))
        except:
            pass

    return error_list

def validate_start_end_elements(starts, ends, mpicc, debug):
    starts = filter(lambda f: not f.is_attempted() and not f.is_validated(), starts)
    ends   = filter(lambda f: not f.is_attempted() and not f.is_validated(), ends)

    for start in starts:
        for end in ends:
            start.attempt()
            end.attempt()

            # this is the graph we are validating
            # sub graph generation via walking database graph
            endpoint_list = [start, end]

            # hash, unique name no other test has
            test_name = start.function_name + "__" + end.function_name

            # Generates test based on the current subgraph
            generate_test(test_name + ".c", endpoint_list)

            stdout, stderr = run_test(test_name,
                                      mpicc_command=mpicc,
                                      debug=debug)

            if not stderr:
                start.validate()
                end.validate()

                logging.warning('validated %s', start.function_name)
                logging.warning('validated %s', end.function_name)

            else:
                logging.warning('failed %s', start.function_name)
                logging.warning('failed %s', end.function_name)

def main():
    """
    Runtime function for Lemonspotter.
    """

    # parse arguments from command line
    arguments = parse_arguments()

    # set logging level
    loglevel = arguments.log
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level)

    # parse given database
    functions = parse_functions(arguments.load + 'defaults.json', arguments.load + 'functions')
    
    types = parse_types(arguments.load + 'types')
    constants = parse_constants(arguments.load + 'constants.json')
    errors = parse_errors(arguments.load + 'errors.json')

    starts = filter(lambda f: not f._needs_all and not f._needs_any, functions)
    ends = filter(lambda f: not f._leads_all and not f._leads_any, functions)
    intermediate = filter(lambda f: (f._needs_all or f._needs_any) and
                                    (f._leads_all or f._leads_any),
                                    functions)

    #constructors = filter(lambda f: f.pa
    #print(list(constructors))

    # validate start and end points
    validate_start_end_elements(starts, ends, arguments.mpi_command, arguments.debug)

    # Runs tests of all functions through all start/end points
#    for start in start_points:
#        # Ensures that this start point is tested and valid
#        if start.get_validation():
#
#            for end in end_points:
#                # Ensures that this endpoint is tested and valid
#                if end.get_validation():
#
#                    for element in elements:
#                        current_test = [start, element, end]
#
#                        """
#                        TODO: Dependencies need to be loaded here.
#                              Can be done recursively from element.
#                              Iterate across all elements that the function
#                              depends on. Then recursively do the same until there
#                              are no more.
#
#                              A clean up step might be needed. Its possible that functions
#                              will be duplicated.
#                        """
#
#                        test_name = element.get_name()
#
#                        generate_test(test_name + ".c", current_test)
#
#                        stdout, stderr = run_test(test_name,
#                                                  mpicc_command=arguments.mpi_command,
#                                                  debug=arguments.debug)
#
#                        if not stderr:
#                            #log(test_name, "pass")
#                            logging.info('validated %s', test_name)
#                        else:
#                            #log(test_name, "fail")
#                            logging.warning('failed %s', test_name)

if __name__ == "__main__":
    main()
