import YTechCode_interpreter
import YTechCode_lexer
import YTechCode_parser

while True:
    string = input('YTech >> ')
    if string != '':
        result, error = YTechCode_interpreter.run('<stdin>',string)
        if error: print(error.error_string())
        elif result: print(repr(result))
    else:
        pass