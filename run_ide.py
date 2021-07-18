import YTechCode_interpreter
import os


def run_ide(filename):
    f = open (filename, "r")
    program = f.read()
    result, error = YTechCode_interpreter.run(str(filename), program)
    if error: print(error.error_string())
    elif result: 
        if len(result.list_elements) == 1:
            print(repr(result.list_elements[0]))
        else:
            pass


    