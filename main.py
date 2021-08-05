#!/usr/bin/env python3
"""Shoggoth - Tools for Java Autograding"""
__author__ = "Ruben Acuna"

import os
import shutil

import javalang
import json


def extract_imports(filename):
    with open(filename, "r") as file:
        data = file.read()
        cu = javalang.parse.parse(data)
        packages = [(p.path, p.wildcard) for p in cu.imports]
        return packages


def find_disallowed_packages(filepaths, whitelist):
    packages = set()

    # find all packages in use
    for filename in filepaths:
        if os.path.isfile(filename):
            packages.update(extract_imports(filename))

    disallowed = [p for p in packages if p[0] not in whitelist or p[1]]

    return disallowed


def body_has_repetition(method_name, body):
    if not body:
        return False
    elif type(body) is list:
        for statement in body:
            if statement_has_repetition(method_name, statement):
                return True
        return False
    else:
        return statement_has_repetition(method_name, body)


def statement_has_repetition(method_name, statement):
    # see https://github.com/c2nes/javalang/blob/master/javalang/tree.py

    if type(statement) in [javalang.tree.IfStatement]:
        return body_has_repetition(method_name, statement.then_statement) or \
               body_has_repetition(method_name, statement.else_statement)
    elif type(statement) is javalang.tree.BlockStatement:
        return body_has_repetition(method_name, statement.statements)
    elif type(statement) in [javalang.tree.WhileStatement, javalang.tree.ForStatement, javalang.tree.DoStatement]:
        return True
    elif type(statement) is javalang.tree.StatementExpression:  # recursion
        if statement.expression.member == method_name:
            return True
    elif type(statement) in [javalang.tree.LocalVariableDeclaration, javalang.tree.ReturnStatement,
                             javalang.tree.AssertStatement, javalang.tree.BreakStatement, javalang.tree.ContinueStatement,
                             javalang.tree.ReturnStatement, javalang.tree.ThrowStatement, javalang.tree.SynchronizedStatement,
                             javalang.tree.TryStatement, javalang.tree.SwitchStatement]:
        pass
    else:
        print("DEBUG: unknown statement encountered in statement_has_iteration: " + str(type(statement)))

    return False


def assert_perf_constant_file(filename, methods):

    r = []
    with open(filename, "r") as file:
        data = file.read()
        cu = javalang.parse.parse(data)

        # can probably can do this on MethodDeclaration but this way prepares us for checking per class.
        for path, node_class in cu.filter(javalang.tree.ClassDeclaration):
            for node_method in node_class.methods:
                name = node_method.name
                if body_has_repetition(name, node_method.body) and name in methods:
                    r += [name]

    return r


def assert_perf_constant(filepaths, methods):
    violations = []
    for filename in filepaths:
        if os.path.isfile(filename):
            violations += assert_perf_constant_file(filename, methods)
    return violations


if __name__ == "__main__":
    #filepaths = ["CompletedDeque.java"]
    #config = {}; config["assert_perf_constant"] = ["toString"] #["enqueueFront"]
    #violations = assert_perf_constant(filepaths, config["assert_perf_constant"])
    #print(violations)
    #exit()

    with open("config.json") as file:
        config = json.load(file)

    # verify and copy required files.
    for required in config["files_required"]:
        filepath_required = config["submission_location"] + required
        if not os.path.isfile(filepath_required):
            print("shoggoth: {} does not exist.".format(filepath_required))
            shutil.copy("/autograder/source/result_missing.json", config["filepath_results"])
            exit()
        else:
            shutil.copy(filepath_required, config["project_location"])

    print("shoggoth: all required files exist.")

    # copy any optional files
    for optional in config["files_optional"]:
        filepath_optional = config["submission_location"] + optional
        if os.path.isfile(filepath_optional):
            shutil.copy(filepath_optional, config["project_location"])

    ret = os.system("mvn -q compile")

    # check if compilation failed
    if ret:
        shutil.copy("/autograder/source/result_buildfail.json", config["filepath_results"])
        exit()
    else:
        filepath_initial_results = "/autograder/results/results_wip.json"
        os.system("mvn -q exec:java > " + filepath_initial_results)

    # compilation succeeded, apply grading rules.
    with open(filepath_initial_results) as file:
        results = json.load(file)
        filepaths = [config["project_location"] + f for f in config["files_required"] + config["files_optional"]]

        # 1) check for disallowed packages and zero scores if any are found.
        disallowed_packages = find_disallowed_packages(filepaths, config["package_whitelist"])
        if disallowed_packages:

            disallowed_packages_insert = {'name': 'Disallowed packages used.',
                                          'number': '0',
                                          'score': 0.0,
                                          'max_score': 0.0,
                                          'visibility': 'visible',
                                          'output': str([p[0] for p in disallowed_packages])}

            for test in results["tests"]:
                test["score"] = 0.0
                test["output"] = ""

            results["tests"].append(disallowed_packages_insert)

        # 2) assert O(1) requirement
        violations = assert_perf_constant(filepaths, config["assert_perf_constant"])
        print(violations)

        with open(config["filepath_results"], 'w') as outfile:
            json.dump(results, outfile)
