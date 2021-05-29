import YTechCode_lexer

while True:
    text = input('YtechCode > ')
    result, error = lexer.run(text)
    if error: print (error.error_string())
    else: print(result)