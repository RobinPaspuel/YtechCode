## DEFINING TOKENS FOR THE LANGUAGE ##
TK_INT = 'TK_INT'
TK_FLOAT = 'FLOAT'
TK_PLUS = 'PLUS'
TK_MINUS ='MINUS'
TK_MUL = 'MUL'
TK_DIV = 'DIV'
TK_LPAREN = 'LPAREN'
TK_RPAREN = 'RPAREN'
TK_SCOLON = 'SCOLON'
TK_EOF = 'EOF'
###################################
DIGITS = '0123456789'
###################################

##### ERRORS ########
class Error:
    def __(self, error_class, details):
        self.error_class= error_class
        self.details= details
    
    def error_string(self):
        result = f'{self.error_class}: {self.details}'
        return result

class IllegalCharacter(Error):
    def __init__(self, details):
        super().__init__('Illegal Character', details)

##################################

class Token:
    def __init__(self, type_, value= None):
        self.type = type_
        self.value = value
    ## Looks better in the terminal
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

## LEXER ##

class Lexer:
    def __init__(self, string):
        self.string = string
        self.pos = -1
        self.current_character = None
        self.advance()

    def advance(self):
        self.pos = + 1
        self.current_character = self.string[self.pos] if self.pos < len(self.string) else None

    def create_tokens(self):
        tokens = []
        while self.current_character != None:
            if self.current_character in '  /t': #Ignoring tab and spaces
                self.advance()
            elif self.current_character in DIGITS:  ##WE define what a number is in the number method
                tokens.append(self.number())
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
                IChar = self.current_character
                self.advance()
                return [], IllegalCharacter("->" + IChar + "<-")
            
        return tokens, None

    def number(self):
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
def run(string):
    lexer = Lexer(string)
    tokens, error = lexer.create_tokens()

    return tokens, error
        