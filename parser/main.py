import lexer
from token import *
import ast

import json
import importlib
import importlib
import json

import sys

def test_function(module_name, function_name, expected_return, num_repetitions, *args):
    module = importlib.import_module(module_name)
    function = getattr(module, function_name)

    for i in range(num_repetitions):
        try:
            if len(args) > 0:
                result = function(*args)
            else:
                result = function()

            if expected_return != "void" and result != expected_return:
                print(f"Test failed for function {function_name}. Expected {expected_return}, but got {result}.")
            else:
                print(f"Test passed for function {function_name}.")
        except Exception as e:
            print(f"Test failed for function {function_name}. Exception thrown: {e}")


def test_functions(module_name, tests_json):
    tests = json.loads(tests_json)
    suite = tests["suite"]
    suite_name = suite["name"]
    tests = suite["tests"]
    execution_order = suite.get("executionOrder", [])

    tested_functions = set()

    # Execute tests in the order specified in the input
    for function_name in execution_order:
        for test in tests:
            if test["name"] == function_name:
                expected_return = test["result"]
                args = [param["value"] for param in test.get("params", [])]
                num_repetitions = test.get("num_repetitions", 1)

                if test.get("-skip"):
                    continue

                test_function(module_name, function_name, expected_return, num_repetitions, *args)
                tested_functions.add(function_name)

    # Execute remaining tests in any order
    for test in tests:
        function_name = test["name"]
        if function_name not in tested_functions:
            expected_return = test["result"]
            args = [param["value"] for param in test.get("params", [])]
            num_repetitions = test.get("num_repetitions", 1)

            if test.get("-skip"):
                continue

            test_function(module_name, function_name, expected_return, num_repetitions, *args)
            tested_functions.add(function_name)


def func(filename):
    input = ''

    with open(filename, 'r') as f:
        input = f.read()

    # print(input)

    parsing_tree = ast.AST()
    parsing_tree.get_tokens_from_input(input)

    # print([(t.Literal, t.Type) for t in parsing_tree.stack])
    # print()

    parsing_tree.populate()
    # print('\nSyntax:\n')
    test = json.dumps(parsing_tree.syntax, indent=4)
    return test

def get_args():
    if len(sys.argv) < 3:
        print('Too few arguments! Please specify the test file and the module you want to test.')

        return None
    elif len(sys.argv) > 3:
        print('Too many arguments! Please specify only the test file and the module you want to test.')

        return None
    
    if '.test' not in sys.argv[1]:
        print('The test file should be of .test extension.')

        return None

    if '.py' not in sys.argv[2]:
        print('The module should be of .py extension.')

        return None
    
    if '.test' in sys.argv[2] and '.py' in sys.argv[1]:
        print('It appears you have confused the test file and the module file.')
    
        return None
    
    return sys.argv[1:]

if __name__ == '__main__':
    test_file, module = get_args()

    tests_json = func(test_file)
    test_functions(module[:-3], tests_json)