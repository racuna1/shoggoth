
import os
import replace_main
import detect_globals
import replace_main
import convert_unit_tests
import whitelist
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
            if detect_globals(filepath_required):
                gsr.add_note("Global Variable", "Global variable detected in {}. Global Variables are not allowed.".format(required))
            
            shutil.copy(filepath_required, config["project_location"])

    

