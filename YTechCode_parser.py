from YTechCode_lexer import *

##### DEFINING NODES ########

class Node_number:
    def __init__(self, token):
        self.token = token
        self.initial_pos = self.token.initial_pos
        self.final_pos = self.token.final_pos

    def __repr__(self):
        return f'{self.token}'

class Node_VarDeclare:
    def __init__(self, variable_name_token):
        self.variable_name_token = variable_name_token

        self.initial_pos = self.variable_name_token.initial_pos
        self.final_pos = self.variable_name_token.final_pos

class Node_VarAssign:
    def __init__(self, variable_name_token, value_node):
        self.variable_name_token = variable_name_token
        self.value_node = value_node

        self.initial_pos = self.variable_name_token.initial_pos
        self.final_pos = self.value_node.final_pos

class Node_Binary_op:
    def __init__(self, left_node, operator_token, right_node):
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node

        self.initial_pos = self.left_node.initial_pos
        self.final_pos = self.right_node.final_pos

    def __repr__(self):
        return f'({self.left_node}, {self.operator_token}, {self.right_node})'

class Node_Unitary_op:
    def __init__(self, operator_token, node):
        self.operator_token = operator_token
        self.node = node

        self.initial_pos = self.operator_token.initial_pos
        self.final_pos = self.node.final_pos

    def __repr__(self):
        return f'({self.operator_token}, {self.node})'

########## PARSER CHECKER ##############

class ParserChecker:
    def __init__(self):
        self.error = None
        self.node  = None
        self.advance_step = 0

    def check_advance(self):
        self.advance_step += 1


    def check(self, result):
        self.advance_step += result.advance_step
        if result.error: self.error = result.error
        return result.node
        

    def check_pass(self, node):
        self.node = node
        return self

    def check_fail(self, error):
        if not self.error or self.advance_step == 0:
            self.error = error
        return self

######## PARSER ##########

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.advance()

    def advance(self, ):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def parse(self):
        result = self.expr()
        if not result.error and self.current_token.type !=  TK_EOF:
            return result.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                "Expected '+', '-', '*' or '/' in -> "
            ))
        return result

    def atom(self):
        result = ParserChecker()
        token = self.current_token

        if token.type in (TK_INT, TK_FLOAT):
            result.check_advance()
            self.advance()
            return result.check_pass(Node_number(token))

        elif token.type == TK_IDENTIFIER:
            result.check_advance()
            self.advance()
            return result.check_pass(Node_VarDeclare(token))

        elif token.type == TK_LPAREN:
            result.check_advance()
            self.advance()
            expr = result.check(self.expr())
            if result.error: return result
            if self.current_token.type == TK_RPAREN:
                result.check_advance()
                self.advance()
                return result.check_pass(expr)
            else: 
                return result.check_fail(InvalidSyntax(
                    self.current_token.initial_pos, self.current_token.final_pos,
                    "Expected ')' in -> "
                ))
        return result.check_fail(InvalidSyntax(
            self.current_token.initial_pos, self.current_token.final_pos,
            "Expected INT, FLOAT, IDENTIFIER,  '+', '-' or '(' in -> "
        ))
    
    def power(self):
        return self.bin_operator(self.atom, (TK_POW, ), self.factor)

    def factor(self):
        result = ParserChecker()
        token = self.current_token

        if token.type in (TK_PLUS, TK_MINUS):
            result.check_advance()
            self.advance()
            factor = result.check(self.factor())
            if result.error: return result
            return result.check_pass(Node_Unitary_op(token, factor))

        return self.power()

    def term(self):
        return self.bin_operator(self.factor, (TK_MUL, TK_DIV))

    def expr(self):
        result = ParserChecker()
        if (self.current_token.matches(TK_KEYWORD, 'let')) or (self.current_token.matches(TK_KEYWORD, 'LET')):
            result.check_advance()
            self.advance()
            if self.current_token.type != TK_IDENTIFIER:
                return result.check_fail(InvalidSyntax(
                    self.current_token.initial_pos, self.current_token.final_pos,
                    'Expected a valid variable name  in -> '
                ))
            variable_name = self.current_token
            result.check_advance()
            self.advance()
        
            if self.current_token.type != TK_EQUALS:
                return result.check_fail(InvalidSyntax(
                    self.current_token.initial_pos, self.current_token.final_pos,
                    "Expected '=' in -> "
                ))
            result.check_advance()
            self.advance()
            expr = result.check(self.expr())
            if result.error: return result
            return result.check_pass(Node_VarAssign(variable_name, expr))

        node = result.check(self.bin_operator(self.term, (TK_PLUS, TK_MINUS)))
        if result.error: 
            return result.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                "Expected 'LET or let', INT, FLOAT, IDENTIFIER, '+', '-', or '(' in -> "
            ))
        return result.check_pass(node)

    def bin_operator(self, function_one, operators, function_two=None):
        if function_two == None:
            function_two = function_one
        result = ParserChecker()
        left_side = result.check(function_one())
        if result.error: return result

        while self.current_token.type in operators:
            operation_token = self.current_token
            result.check_advance()
            self.advance()
            right_side = result.check(function_two())
            if result.error: return result
            left_side = Node_Binary_op(left_side,operation_token, right_side)
        return result.check_pass(left_side)

