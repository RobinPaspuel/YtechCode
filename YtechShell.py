import YTechCode_lexer

while True:
    string = input('YtechCode > ')
    result, error = YTechCode_lexer.run('<stdin>',string)

    if error: print(error.error_string())
    else: print(result)