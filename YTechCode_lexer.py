from error_handlrer import *
###################################
DIGITS = '0123456789'
###################################


### POSITION MANAGEMENT #####

class Position:
    def __init__(self, index, line, column, filename, filetext):
        self.index= index
        self.line= line
        self.column= column
        self.filename= filename
        self.filetext= filetext
    
    def advance(self, current_character = None):
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
    def __init__(self, type, value=None, initial_pos=None, final_pos=None):
        self.type = type
        self.value = value
        
        if initial_pos: 
            self.initial_pos = initial_pos.copy()
            self.final_pos = initial_pos.copy()
            self.final_pos.advance()
        if final_pos:
            self.final_pos = final_pos.copy()

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
                tokens.append(Token(TK_PLUS, initial_pos = self.pos))
                self.advance()
            elif self.current_character == '-':
                tokens.append(Token(TK_MINUS, initial_pos = self.pos))
                self.advance()
            elif self.current_character == '*':
                tokens.append(Token(TK_MUL, initial_pos = self.pos))
                self.advance()
            elif self.current_character == '/':
                tokens.append(Token(TK_DIV,  initial_pos = self.pos))
                self.advance()
            elif self.current_character == '(':
                tokens.append(Token(TK_LPAREN, initial_pos = self.pos))
                self.advance()
            elif self.current_character == ')':
                tokens.append(Token(TK_RPAREN, initial_pos = self.pos))
                self.advance()
            elif self.current_character == ';':
                tokens.append(Token(TK_SCOLON, initial_pos = self.pos))
                self.advance()
            else:
                initial_pos = self.pos.copy()
                IChar = self.current_character
                self.advance()
                return [], IllegalCharacter(initial_pos, self.pos,"-> " + IChar + " in -> ")
            
        tokens.append(Token(TK_EOF,initial_pos = self.pos))
        return tokens, None

    def make_number(self):
        number_str = ''
        dots = 0
        initial_pos = self.pos.copy()

        while self.current_character != None and self.current_character in DIGITS + '.':
            if self.current_character == '.':
                if dots == 1: break
                dots += 1
                number_str += '.'
            else:
                number_str += self.current_character
            self.advance()
            
        if dots == 0: 
            return Token(TK_INT, int(number_str), initial_pos, self.pos)
        else:
            return Token(TK_FLOAT, float(number_str), initial_pos, self.pos)

##### Temporal run function #####

        