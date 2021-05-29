###################################
DIGITS = '0123456789'
###################################

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
        return result

class IllegalCharacter(Error):
    def __init__(self,initial_pos, final_pos, details):
        super().__init__(initial_pos, final_pos, 'Illegal Character', details)

##################################
### POSITION MANAGEMENT #####

class Position:
    def __init__(self, index, line, column, filename, filetext):
        self.index= index
        self.line= line
        self.column= column
        self.filename= filename
        self.filetext= filetext
    
    def advance(self, current_character):
        self.index += 1
        self.column += 1

        if current_character == '\n':
            self.line += 1
            self.column = 0
        return self
    
    def copy(self):
        return Position(self.index, self.line, self.column, self.filename, self.filetext)

##############################

## DEFINING TOKENS FOR THE LANGUAGE ##
TK_INT = 'INT'
TK_FLOAT = 'FLOAT'
TK_PLUS = 'PLUS'
TK_MINUS ='MINUS'
TK_MUL = 'MUL'
TK_DIV = 'DIV'
TK_LPAREN = 'LPAREN'
TK_RPAREN = 'RPAREN'
TK_SCOLON = 'SCOLON'
TK_EOF = 'EOF'
####################################



class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

## LEXER ##

class Lexer:
    def __init__(self, filename, string):
        self.filename = filename
        self.string = string
        self.pos = Position(-1, 0, -1, filename, string)
        self.current_character = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_character)
        self.current_character = self.string[self.pos.index] if self.pos.index < len(self.string) else None

    def create_tokens(self):
        tokens = []

        while self.current_character != None:
            if self.current_character in ' \t': #Ignoring tab and spaces
                self.advance()
            elif self.current_character in DIGITS:  ##WE define what a number is in the number method
                tokens.append(self.make_number())
            elif self.current_character == '+':
                tokens.append(Token(TK_PLUS))
                self.advance()
            elif self.current_character == '-':
                tokens.append(Token(TK_MINUS))
                self.advance()
            elif self.current_character == '*':
                tokens.append(Token(TK_MUL))
                self.advance()
            elif self.current_character == '/':
                tokens.append(Token(TK_DIV))
                self.advance()
            elif self.current_character == '(':
                tokens.append(Token(TK_LPAREN))
                self.advance()
            elif self.current_character == ')':
                tokens.append(Token(TK_RPAREN))
                self.advance()
            elif self.current_character == ';':
                tokens.append(Token(TK_SCOLON))
                self.advance()
            else:
                initial_pos = self.pos.copy()
                IChar = self.current_character
                self.advance()
                return [], IllegalCharacter(initial_pos, self.pos,"-> " + IChar + " in -> ")
            
        return tokens, None

    def make_number(self):
        number_str = ''
        dots = 0

        while self.current_character != None and self.current_character in DIGITS + '.':
            if self.current_character == '.':
                if dots == 1: break
                dots += 1
                number_str += '.'
            else:
                number_str += self.current_character
            self.advance()
            
        if dots == 0: 
            return Token(TK_INT, int(number_str))
        else:
            return Token(TK_FLOAT, float(number_str))

##### Temporal run function #####
def run(filename, string):
    lexer = Lexer(filename, string)
    tokens, error = lexer.create_tokens()

    return tokens, error
        