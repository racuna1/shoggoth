import os
import shutil
import javalang
import analysis_java_perf

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


def body_has_repetition(class_name, method_name, body):
    if not body:
        return False
    elif type(body) is list:
        for statement in body:
            if statement_has_repetition(class_name, method_name, statement):
                return True
        return False
    else:
        return statement_has_repetition(class_name, method_name, body)


def follows_constant_rule(cu, method):
    # can probably can do this on MethodDeclaration but this way prepares us for checking per class.
    for path, node_class in cu.filter(javalang.tree.ClassDeclaration):
        for node_method in node_class.methods:
            method_name = node_method.name
            if body_has_repetition(node_class.name, method_name, node_method.body) and method_name == method:
                return False

    return True


def assert_perf_constant_rules(gsr, filepaths, parse_trees, methods):
    for filename in filepaths:
        cu = parse_trees[filename]
        for method in methods:
            if not follows_constant_rule(cu, method):
                note = "{}::{} Did not meet O(1) performance requirement.".format(os.path.basename(filename), method)
                gsr.zero_by_keyword(method, note)


def follows_linear_rule(cu, method):
    # can probably can do this on MethodDeclaration but this way prepares us for checking per class.
    for path, node_class in cu.filter(javalang.tree.ClassDeclaration):
        for node_method in node_class.methods:
            method_name = node_method.name
            est = analysis_java_perf.body_est_order(node_class.name, method_name, node_method.body)
            #print("DEBUG:" + str(method_name) + " is O(" + str(est)+")")
            if est > 1 and method_name == method:
                return False

    return True

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
        c_grader.grade(config, gsr)
    # Java testing
    else:
        java_grader.grade(config, gsr)

    gsr.save(config["filepath_results"])
def assert_perf_linear_rules(gsr, filepaths, parse_trees, methods):
    for filename in filepaths:
        cu = parse_trees[filename]
        for method in methods:
            if not follows_linear_rule(cu, method):
                note = "{}::{} Found nested loops. Most likely does not meet O(n) performance requirement.".format(os.path.basename(filename), method)
                gsr.zero_by_keyword(method, note)


def assert_no_class_variables(gsr, filepaths, parse_trees, classes):
    for filename in filepaths:
        cu = parse_trees[filename]
        for path, node_class in cu.filter(javalang.tree.ClassDeclaration):

            if node_class.name in classes and len(node_class.fields) > 0:
                gsr.zero_all()
                note = "{}: Found class member variables.".format(node_class.name)
                gsr.add_note(note, "")
                #gsr.add_note("Disallowed packages used.", str([p[0] for p in disallowed_packages]))


def grade(config, gsr):
    # verify and copy required files.
    for required in config["files_required"]:
        filepath_required = config["submission_location"] + required
        if not os.path.isfile(filepath_required):
            print("shoggoth: {} does not exist.".format(filepath_required))
            gsr.set_result_filemissing()
            gsr.save(config["filepath_results"])
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
        gsr.set_result_buildfail()
    else:
        filepath_initial_results = "/autograder/results/results_wip.json"
        os.system("mvn -q exec:java > " + filepath_initial_results)

        # compilation succeeded, apply grading rules.
        gsr.load(filepath_initial_results)
        filepaths = [config["project_location"] +
                     f for f in config["files_required"] + config["files_optional"]]

        # build javalang parse trees for all files
        parse_trees = dict()
        for filepath in filepaths:
            with open(filepath, "r") as file:
                data = file.read()
                cu = javalang.parse.parse(data)
                parse_trees[filepath] = cu

        # 1) check for disallowed packages and zero scores if any are found.
        disallowed_packages = find_disallowed_packages(
            filepaths, config["package_whitelist"])
        if disallowed_packages:
            gsr.zero_all()
            gsr.add_note("Disallowed packages used.", str(
                [p[0] for p in disallowed_packages]))

        # 2) assert O(1) requirement
        assert_perf_constant_rules(
            gsr, filepaths, parse_trees, config["assert_perf_constant"])

        # 3) assert O(n) requirement
        assert_perf_linear_rules(
            gsr, filepaths, parse_trees, config["assert_perf_linear"])

        # 4) assert no class variables
        assert_no_class_variables(
            gsr, filepaths, parse_trees, config["assert_no_class_variables"])
