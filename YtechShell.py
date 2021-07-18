import YTechCode_interpreter
import YTechCode_lexer
import YTechCode_parser

welcome_message = """YTech Code 0.3.1  Built of: Jul 9, 2021
License: MIT\n """
print(welcome_message)
while True:
    string = input('YT >>> ')
    if string != '':
        result, error = YTechCode_interpreter.run('<stdin>',string)
        if error: print(error.error_string())
        elif result: 
            if len(result.list_elements) ==1:
                print(repr(result.list_elements[0]))
            else:
                print(repr(result))
    else:
        pass
