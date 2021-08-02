#!/usr/bin/env python3

__author__ = "Ruben Acuna"

import os
import javalang
import simplejson


def extract_imports(filename):
    with open(filename, "r") as file:
        data = file.read()
        cu = javalang.parse.parse(data)
        packages = [(p.path, p.wildcard) for p in cu.imports]
        return packages


def validate_packages(whitelist):
    packages = set()

    # find all packages in use
    for filename in config["files_required"] + config["files_optional"]:
        # print(filename)
        if os.path.isfile(filename):
            packages.update(extract_imports(filename))

    for package in packages:
        if package[0] not in whitelist or package[1]:
            return False

    return True


if __name__ == "__main__":
    with open("config.json") as file:
        config = simplejson.load(file)

    extract_imports("CompletedDeque.java")

    print(validate_packages(config["package_whitelist"]))
