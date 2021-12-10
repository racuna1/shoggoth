__author__ = "Charles Jeffries"

import gradescope_result
import xml.etree.ElementTree as ET
import re

def parseXML(file):
    tree = ET.parse(file)

    root = tree.getroot()

    testResults = []

    num = 0

    for testCase in root.findall('testcase'):
        result = {}

        result['name'] = testCase.get('name')
        result['time'] = testCase.get('time')
        result['failCount'] = 0
        
        failures = []

        for failure in testCase.findall('failure'):
            fail = {}
            fail['message'] = re.sub("\{newline\}", "\n", failure.get('message'))
            result['failCount'] = result.get('failCount') + 1
            failures.append(fail)
        
        result['failures'] = failures
        result['testNum'] = num

        testResults.append(result)
        num += 1

    return testResults
    

if __name__ == "__main__":
    testResults = parseXML('./SERXXX_AssignmentNum_Test_Project/tests/cpputest_tests.xml')

    #print(testResults);

    gr = gradescope_result.GradescopeResult()
    
    for tr in testResults:
        if tr['failCount'] > 0:
            gr.add_test_result(tr['name'], 0, 1, 'Failed ' + str(tr['failCount']) + ' test cases.')
        else:
            gr.add_test_result(tr['name'], 1, 1, 'Passed all test cases.')
    
    gr.save('/autograder/results/results.json')

