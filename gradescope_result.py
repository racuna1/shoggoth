import json


class GradescopeResult:
    """
    A wrapper for a Gradescope result file that provides common operations.
    """

    def __init__(self, infilepath, outfilepath):
        with open(infilepath) as infile:
            self.results = json.load(infile)

        self.outfilepath = outfilepath

    def add_note(self, name,  output):
        new_entry = {'name': name,
                     'number': '0',
                     'score': 0.0,
                     'max_score': 0.0,
                     'visibility': 'visible',
                     'output': output}

        self.results["tests"].append(new_entry)

    def zero_all(self):
        for test in self.results["tests"]:
            test["score"] = 0.0
            test["output"] = ""

    def zero_by_keyword(self, keyword, output, append=False):
        for test in self.results["tests"]:
            if keyword in test["name"]:
                test["score"] = 0.0
                if append:
                    test["output"] += "\n" + output
                else:
                    test["output"] = output

    def save(self, filepath):
        with open(self.outfilepath, 'w') as outfile:
            json.dump(self.results, outfile)