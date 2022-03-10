import src.YTechCode_interpreter as YTechCode_interpreter

welcome_message = """YTech Code 0.3.3  Built of: Jul 26, 2021
License: MIT\n """
print(welcome_message)
while True:
    string = input('YT >>> ')
    if string != '':
        result, error = YTechCode_interpreter.run('<stdin>', string)
        if error:
            print(error.error_string())
        elif result:
            if len(result.list_elements) == 1:
                print(repr(result.list_elements[0]))
            else:
                print(repr(result))
