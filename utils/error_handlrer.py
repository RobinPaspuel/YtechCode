
from utils.error_with_arrows import *
##### ERRORS ########
class Error:
    def __init__(self, initial_pos, final_pos, error_class, details):
        self.initial_pos = initial_pos
        self.final_pos = final_pos
        self.error_class= error_class
        self.details= details
    
    def error_string(self):
        result = f'{self.error_class}: {self.details}'
        result += f'File {self.initial_pos.filename} at line: {self.initial_pos.line + 1}'
        result += '\n\n' + string_with_arrows(self.initial_pos.filetext, self.initial_pos, self.final_pos)
        return result

class IllegalCharacter(Error):
    def __init__(self,initial_pos, final_pos, details):
        super().__init__(initial_pos, final_pos, 'Illegal Character', details)

class ExpectedCharacterError(Error):
    def __init__(self,initial_pos, final_pos, details):
        super().__init__(initial_pos, final_pos, 'Expected Character', details)

class InvalidSyntax(Error):
    def __init__(self,initial_pos, final_pos, details = ''):
        super().__init__(initial_pos, final_pos, 'Invalid Syntax', details)

class RunTimeError(Error):
    def __init__(self, initial_pos, final_pos, details, context):
        super().__init__(initial_pos, final_pos, 'Runtime Error', details)
        self.context = context
    
    def error_string(self):
        result = self.generate_traceback()
        result += f'{self.error_class}: {self.details}\n'
        result += '\n\n' + string_with_arrows(self.initial_pos.filetext, self.initial_pos, self.final_pos)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.initial_pos
        ctx  = self.context
        while ctx:
            result = f'  File {pos.filename}, line {str(pos.line + 1)}, in {ctx.context_name}\n' + result
            pos = ctx.context_parent_entry_pos
            ctx = ctx.context_parent
        return 'Traceback (most recent call last):\n' + result
##################################