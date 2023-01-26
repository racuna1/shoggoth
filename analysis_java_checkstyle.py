"""
Shoggoth - A Gradescope compatible tool for performing automatic assessment of Java homework, using static and
dynamic analysis.
"""
__author__ = "Ruben Acuna"

import os
import gradescope_result
import xml.etree.ElementTree as ET


def evaluate(gsr, grading_rules):
    filename_report = "target" + os.sep + "checkstyle-result.xml"

    # no report means skip evaluation
    if not os.path.exists(filename_report):
        return

    uncaught_errors = []
    rule_violations = {}

    tree = ET.parse(filename_report)

    for file in tree.getroot():
        src_file = file.attrib["name"]
        src_file = src_file.split(os.sep)[-1]

        # TODO: may need to support warnings as well

        for error in file:
            line = error.attrib["line"]
            column = error.attrib["column"]
            severity = error.attrib["severity"]
            message = error.attrib["message"]
            source = error.attrib["source"]

            # com.puppycrawl.tools.checkstyle.checks.naming.LocalVariableNameCheck -> LocalVariableNameCheck
            category = source.split(".")[-2]
            #                                                                      -> naming
            rule = source.split(".")[-1]

            # LocalVariableNameCheck -> LocalVariableNameCheck
            if category == "naming":
                rule = rule[:-5]  # remove Check suffix

            # formatted like html
            # print(severity, category, rule, message, line)

            # three options: start new, continue existing, or put into bucket.
            if rule in rule_violations:
                rule_violations[rule] += f"\nFile: {src_file}, Severity: {severity}, Category: {category}, Rule: {rule}, Message: {message}, Line: {line}"
            else:
                grading_rule = None
                for gr in grading_rules:
                    if gr["name"] == rule:
                        grading_rule = rule
                        break

                if grading_rule:
                    rule_violations[rule] = f"File: {src_file}, Severity: {severity}, Category: {category}, Rule: {rule}, Message: {message}, Line: {line}"
                else:
                    uncaught_errors.append((src_file, severity, category, rule, message, line))

    # add a note for each rule violation
    for gr in grading_rules:
        if gr["name"] in rule_violations:
            # lost credit
            gsr.add_case(f"Checkstyle Rule: {gr['name']}", 0, gr["max_score"], rule_violations[gr["name"]])
        else:
            # earned credit
            gsr.add_case(f"Checkstyle Rule: {gr['name']}", gr["max_score"], gr["max_score"], "")

    # add a note about any uncaught errors
    uncaught_message = f"Checkstyle has identified {len(uncaught_errors)} additional errors. These errors are not worth points and are only informative:"

    for src_file, severity, category, rule, message, line in uncaught_errors:
        message = f"\nFile: {src_file}, Severity: {severity}, Category: {category}, Rule: {rule}, Message: {message}, Line: {line}"
        uncaught_message += message
    gsr.add_note("Checkstyle Overall", uncaught_message)

    #print(uncaught_message)
    #print(gsr.results)


if __name__ == "__main__":
    rules = [{"name": "LocalVariableName", "max_score": 1.0}, {"name": "MadeUpRuleName", "max_score": 1.0}]

    result = gradescope_result.GradescopeResult()
    #may need info from config file as well

    evaluate(result, rules)