import os
import shutil
import json

# C imports
from replace_main import rename_main
from detect_globals import detect_globals
from convert_unit_tests import parseXML
from whitelist import scan_disallowed


def grade(config, gsr):
    # verify and copy required files.
    for required in config["files_required"]:
        print("verifying file " + required) 
        filepath_required = config["submission_location"] + required
        if not os.path.isfile(filepath_required):
            print("shoggoth: {} does not exist.".format(filepath_required))
            gsr.set_result_filemissing()
            gsr.save(config["filepath_results"])
            exit()
        else:
            if config["prohibit_globals"]:
                if detect_globals(filepath_required):
                    gsr.add_note(
                        "Global Variable", "Global variable detected in {}. Global Variables are not allowed.".format(required))

            if scan_disallowed(config["submission_location"], config["whitelist"]):
                gsr.set_result_illegalincludes(config["whitelist"])
                gsr.save(config["filepath_results"])
                exit()

            if required == config["main_file"]:
                print("renaming main method")
                rename_main(filepath_required)

            shutil.copy(filepath_required,
                        config["project_location"] + "src/code/")

    status = os.system("cd " + config["project_location"] + "; make all")

    # CJ
    # from my testing I think status is 1 if compilation fails, and 2 if tests fail, and 0 if all are good
    if status == 1:
        gsr.set_result_buildfail()
        gsr.save(config["filepath_results"])
        exit()
    elif status == 2:
        gsr.add_note("Note", "Some tests may have failed.")


    #CJ: We check if ithe test results were generated, if they weren't then the program likely crashed.
    try:
        shutil.copy(config["project_location"] + "tests/cpputest_tests.xml", "/autograder/source/test_results/")
    except IOError as e:
        gsr.add_note("Error", "The Program did not execute successfully (likely a segmentation fault or other runtime error occurred).")
        gsr.save(config["filepath_results"])
        exit()

    
    testResults = parseXML(
        "/autograder/source/test_results/cpputest_tests.xml")

    for tr in testResults:
        val = 0
        for ut in config["unit_tests"]:
            if(ut["name"] == tr['name']):
                val = ut["points"]
        if tr['failCount'] > 0:
            messageString = ""
            messageString += 'Failed ' + str(tr['failCount']) + ' test cases.\n'
            for failure in tr['failures']:
                messageString += failure['message']
            gsr.add_test_result(
                tr['name'], 0, val, 'Failed ' + str(tr['failCount']) + ' test cases.')
        else:
            gsr.add_test_result(tr['name'], val, val, 'Passed all test cases.')
