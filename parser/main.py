import lexer
from token import *
import ast

import json
import importlib
import importlib
import json

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


def func():
    input = '''
      Suite mySuite

      Test foo1 -repeat 5 times
      When param1=1
      Then result should be 1

      Test foo2 -repeat 2 times
      When param2=True, param3="John"
      Then result should be 0

      Test foo3 
      When no parameters
      Then result should be 1.42

      Execution order: foo3, foo1, foo2
      '''

    parsing_tree = ast.AST()
    parsing_tree.get_tokens_from_input(input)

    print([(t.Literal, t.Type) for t in parsing_tree.stack])
    print()

    parsing_tree.populate()
    print('\nSyntax:\n')
    test = json.dumps(parsing_tree.syntax, indent=4)
    return test


if __name__ == '__main__':
    #print(func())
    tests_json = func()
    test_functions("pbl_test", tests_json)



