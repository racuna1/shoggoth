#!/usr/bin/env python3
"""
Shoggoth - A Gradescope compatible tool for performing automatic assessment of Java homework, using static and
dynamic analysis.
"""
__author__ = "Ruben Acuna"

import os
import shutil
import json

import gradescope_result
import c_grader
import java_grader

if __name__ == "__main__":
    # add manually installed version of maven to path
    os.environ["PATH"] += os.pathsep + "/autograder/apache-maven-3.8.3/bin"

    with open("config.json") as file:
        config = json.load(file)

    gsr = gradescope_result.GradescopeResult()

    # C testing
    if config["mode_c_testing"]:
        print("starting C autograder")
        c_grader.grade(config, gsr)
    # Java testing
    else:
        java_grader.grade(config, gsr)

    gsr.save(config["filepath_results"])
