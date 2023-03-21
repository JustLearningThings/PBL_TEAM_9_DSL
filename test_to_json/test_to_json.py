import re
from textx import metamodel_from_file
import json

mm = metamodel_from_file('./test.tx')
model = mm.model_from_file('./example.test')

test_order = model.order.test_names

output_dict = {"tests": []}

#tests in the order based on the execution order
for test_name in test_order:
    #find corresponding test in the file
    test = next(t for t in model.tests if t.name == test_name)
    test_dict = {"name": test.name, "params": [], "result": str(test.result.value)}
    for param in test.params:
        if param.param_value:
            param_dict = {"param_name": param.param_name, "param_value": str(param.param_value)}
        else:
            param_dict = {"param_name": param.param_name, "param_value": "no parameters"}
        test_dict["params"].append(param_dict)
    output_dict["tests"].append(test_dict)

# output the json file
output_file = open("output.json", "w")
json.dump(output_dict, output_file, indent=4)
output_file.close()
print("Check the output file!")
