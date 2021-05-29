import YTechCode_parser

while True:
    string = input('YtechCode > ')
    ast, error = YTechCode_parser.run('<stdin>',string)

    if error: print(error.error_string())
    else: print(ast)