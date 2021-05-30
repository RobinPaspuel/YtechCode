import YTechCode_interpreter
import YTechCode_lexer
import YTechCode_parser

while True:
    string = input('YtechCode > ')
    result, error = YTechCode_interpreter.run('<stdin>',string)

    if error: print(error.error_string())
    elif result: print(result)