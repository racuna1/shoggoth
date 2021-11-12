import gradescope_result
import xml.etree.ElementTree as ET

def parseXML(file):
    tree = ET.parse(file)

    root = tree.getroot()

    testResults = []

    for testCase in root.findall('testcase'):
        result = {}

        result['name'] = testCase.get('name')
        result['time'] = testCase.get('time')
        result['failCount'] = 0
        
        failures = []

        for failure in testCase.findall('failure'):
            fail = {}
            fail['message'] = failure.get('message')
            result['failCount'] = result.get('failCount') + 1
            failures.append(fail)

        testResults.append(result)

    return testResults
    

        


if __name__ == "__main__":
    foo = 5