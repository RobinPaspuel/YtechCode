import YTechCode_interpreter

while True:
    string = input('YtechCode > ')
    result, error = YTechCode_interpreter.run('<stdin>',string)

    if error: print(error.error_string())
    else: print(result)