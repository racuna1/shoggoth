
import os
from replace_main import rename_main
from detect_globals import detect_globals
from convert_unit_tests import parseXML
from whitelist import scan_disallowed
import json
import gradescope_result_V2
import shutil

if __name__ == "__main__":
    with open("config.json") as file:
        config = json.load(file)

    gsr = gradescope_result_V2.GradescopeResult()

    # verify and copy required files.
    for required in config["files_required"]:
        filepath_required = config["submission_location"] + required
        if not os.path.isfile(filepath_required):
            print("shoggoth: {} does not exist.".format(filepath_required))
            gsr.set_result_filemissing()
            gsr.save(config["filepath_results"])
            exit()
        else:
            if config["prohibit_globals"]:
                if detect_globals(filepath_required):
                    gsr.add_note("Global Variable", "Global variable detected in {}. Global Variables are not allowed.".format(required))
                
            if scan_disallowed(config["submission_location"], config["whitelist"]):
                gsr.set_result_illegalincludes(config["whitelist"])
                gsr.save(config["filepath_results"])
                exit()

            if required == config["main_file"]:
                rename_main(required)

            shutil.copy(filepath_required, config["project_location"] + "src/code/")

    status = os.system("./run_cpputest.sh")

    #CJ
    #from my testing I think status is 1 if compilation fails, and 2 if tests fail, and 0 if all are good
    if status == 1:
        gsr.set_result_buildfail()
        gsr.save(config["filepath_results"])
        exit()
    elif status == 2:
        gsr.add_note("Note", "Some tests may have failed.")

    shutil.copy(config["project_location"] + "tests/cpputest_tests.xml", "/autograder/source/test_results/")

    testResults = parseXML("/autograder/source/test_results/cpputest_tests.xml")

    for tr in testResults:
        if tr['failCount'] > 0:
            gsr.add_test_result(tr['name'], 0, 1, 'Failed ' + str(tr['failCount']) + ' test cases.')
        else:
            gsr.add_test_result(tr['name'], 1, 1, 'Passed all test cases.')
    

    gsr.save(config["filepath_results"])

    

    

