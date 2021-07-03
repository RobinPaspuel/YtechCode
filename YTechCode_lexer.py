from error_handlrer import *
import string
###################################
DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_and_DIGITS = LETTERS + DIGITS
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
TK_INT          = 'INT'
TK_FLOAT        = 'FLOAT'
TK_STRING       = 'STRING'
TK_IDENTIFIER   = 'IDENTIFIER'
TK_KEYWORD      = 'KEYWORD'
TK_EQUALS       = 'EQUALS'
TK_PLUS         = 'PLUS'
TK_MINUS        = 'MINUS'
TK_MUL          = 'MUL'
TK_DIV          = 'DIV'
TK_POW          = 'POW'
TK_LPAREN       = 'LPAREN'
TK_RPAREN       = 'RPAREN'
TK_LSPAREN      = 'LSRAPEN'
TK_RSPAREN      = 'RSPAREN'
TK_DEQ          = 'DEQ'
TK_NDEQ         = 'NDEQ'
TK_LL           = 'LL'
TK_GG           = 'GG'
TK_LEQ          = 'LEQ'
TK_GEQ          = 'GEQ'
TK_CBL          = 'CBL'
TK_CBR          = 'CBR'
TK_SCOLON       = 'SCOLON'
TK_COLON        = 'COLON'
TK_ARROW        = 'ARROW'
TK_COMMA        = 'COMMA'
TK_PIPE         = 'PIPE'
TK_EOF          = 'EOF'

KEYWORDS = [
    'let',
    'LET',
    'and',
    'AND',
    'or', 
    'OR',
    'not',
    'NOT', 
    'IF', 
    'if',
    'ELIF',
    'elif',
    'ELSE',
    'else',
    'FOR',
    'for',
    'WHILE',
    'while',
    'DEF',
    'def',
]
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

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

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
            elif self.current_character in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_character == '+':
                tokens.append(Token(TK_PLUS, initial_pos = self.pos))
                self.advance()
            elif self.current_character == '-':
                tokens.append(self.make_minus_or_equal())
            elif self.current_character == '*':
                tokens.append(Token(TK_MUL, initial_pos = self.pos))
                self.advance()
            elif self.current_character == '/':
                tokens.append(Token(TK_DIV,  initial_pos = self.pos))
                self.advance()
            elif self.current_character == '^':
                tokens.append(Token(TK_POW,  initial_pos = self.pos))
                self.advance()
            elif self.current_character == '(':
                tokens.append(Token(TK_LPAREN, initial_pos = self.pos))
                self.advance()
            elif self.current_character == ')':
                tokens.append(Token(TK_RPAREN, initial_pos = self.pos))
                self.advance()
            elif self.current_character == '[':
                tokens.append(Token(TK_LSPAREN, initial_pos = self.pos))
                self.advance()
            elif self.current_character == ']':
                tokens.append(Token(TK_RSPAREN, initial_pos = self.pos))
                self.advance()
            elif self.current_character == ';':
                tokens.append(Token(TK_SCOLON, initial_pos = self.pos))
                self.advance()
            elif self.current_character == '!':
                token, error = self.make_not_equal()
                if error: return [], error
                tokens.append(token)
            elif self.current_character == '=':
                tokens.append(self.make_equal())
            elif self.current_character == '<':
                tokens.append(self.make_less_than())
            elif self.current_character == '>':
                tokens.append(self.make_grater_than())
            elif self.current_character == '{':
                tokens.append(Token(TK_CBL, initial_pos = self.pos))
                self.advance()
            elif self.current_character == '}':
                tokens.append(Token(TK_CBR, initial_pos = self.pos))
                self.advance()
            elif self.current_character == ':':
                tokens.append(Token(TK_COLON, initial_pos = self.pos))
                self.advance()
            elif self.current_character == ',': 
                tokens.append(Token(TK_COMMA, initial_pos = self.pos))
                self.advance()
            elif self.current_character == '"':
                tokens.append(self.make_string())
            elif self.current_character == '|':
                tokens.append(Token(TK_PIPE, initial_pos = self.pos))
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

    def make_identifier(self):
        identifier_str = ''
        initial_pos = self.pos.copy()
    
        while self.current_character != None and self.current_character in LETTERS_and_DIGITS + '_':
            identifier_str += self.current_character
            self.advance()
        token_type = TK_KEYWORD if identifier_str in KEYWORDS else TK_IDENTIFIER
        return Token(token_type, identifier_str, initial_pos, self.pos)

    def make_not_equal(self):
        initial_pos = self.pos.copy()
        self.advance()

        if self.current_character == '=':
            self.advance()
            return Token(TK_NDEQ, initial_pos = initial_pos, final_pos = self.pos), None
        self.advance()
        return None, ExpectedCharacterError(
            initial_pos, self.pos,
            "Missing '=' after '!' in -> "
        )

    def make_equal(self):
        token_type = TK_EQUALS
        initial_pos = self.pos.copy()
        self.advance()

        if self.current_character == '=':
            self.advance()
            token_type = TK_DEQ
        return Token(token_type, initial_pos = initial_pos, final_pos = self.pos)
    
    def make_less_than(self):
        token_type = TK_LL
        initial_pos = self.pos.copy()
        self.advance()

        if self.current_character == '=':
            self.advance()
            token_type = TK_LEQ
        return Token(token_type, initial_pos = initial_pos, final_pos = self.pos)

    def make_grater_than(self):
        token_type = TK_GG
        initial_pos = self.pos.copy()
        self.advance()

        if self.current_character == '=':
            self.advance()
            token_type = TK_GEQ
        return Token(token_type, initial_pos = initial_pos, final_pos = self.pos)

    def make_minus_or_equal(self):
        token_type = TK_MINUS
        initial_pos = self.pos.copy()
        self.advance()

        if self.current_character == '>':
            self.advance()
            token_type = TK_ARROW
        return Token(token_type, initial_pos = initial_pos, final_pos =self.pos)

    def make_string(self):
        string = ''
        initial_pos = self.pos.copy()
        no_print_character = False
        self.advance()
        
        no_print_characters = {
            'n' : '\n',
            't' : '\t'
        }

        while self.current_character != None and (self.current_character != '"' or no_print_character):
            if no_print_character:
                string += no_print_characters.get(self.current_character, self.current_character)
            else:
                if self.current_character == '\\':
                    no_print_character = True
                else:
                    string += self.current_character
            self.advance()
            no_print_character = False
        
        self.advance()
        return Token(TK_STRING, string, initial_pos = initial_pos, final_pos = self.pos)


##### Temporal run function #####

def lexer_run(filename, text):
    lexer = Lexer(filename, text)
    tokens, error = lexer.create_tokens()

    return tokens, error
        