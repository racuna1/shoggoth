import json
import os
import re

def found_disallowed(path, allowed):
    with open(path, 'r') as file:
        regex = "#include (?P<name><.*>)"
        found = re.finditer(regex, file.read())
        return [i.group("name") for i in found if i.group("name") not in allowed]


def scan_disallowed(filepath, allowed):
    for root, dirs, files in os.walk(filepath):

        for file in files:
            if(found_disallowed('/'.join((root, file)), allowed)):
                return True

        for path in dirs:
            scan_disallowed(root + path, allowed)


if __name__ == "__main__":
    with open("config.json") as file:
        config = json.load(file)

    result = scan_disallowed(config["submission_location"], config["whitelist"])
    print(result)