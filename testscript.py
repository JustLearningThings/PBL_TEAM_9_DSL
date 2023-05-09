import importlib

def test_function(module_name, function_name, expected_return, *args):
    module = importlib.import_module(module_name)
    function = getattr(module, function_name)

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


def test_functions(module_name, tests):
    for test in tests:
        function_name = test["function_name"]
        expected_return = test["expected_return"]
        args = test.get("args", [])

        test_function(module_name, function_name, expected_return, *args)

if __name__=="__main__":
    tests = [
        {
            "function_name": "add_numbers",
            "args": [1, 2],
            "expected_return": 3
        },
        {
            "function_name": "multiply_numbers",
            "args": [3, 4],
            "expected_return": 12
        },
        {
            "function_name": "print_msg",
            "expected_return": "void"
        }
    ]

    test_functions("pbl_test", tests)

