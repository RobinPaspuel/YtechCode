from YTechCode_lexer import *

##### DEFINING NODES ########

class Node_number:
    def __init__(self, token):
        self.token = token
        self.initial_pos = self.token.initial_pos
        self.final_pos = self.token.final_pos

    def __repr__(self):
        return f'{self.token}'

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
    
    def check(self, result):
        if isinstance(result,ParserChecker):
            if result.error: self.error = result.error
            return result.node
        return result

    def check_pass(self, node):
        self.node = node
        return self

    def check_fail(self, error):
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

    def factor(self):
        result = ParserChecker()
        token = self.current_token

        if token.type in (TK_PLUS, TK_MINUS):
            result.check(self.advance())
            factor = result.check(self.factor())
            if result.error: return result
            return result.check_pass(Node_Unitary_op(token, factor))

        elif token.type in (TK_INT, TK_FLOAT):
            result.check(self.advance())
            return result.check_pass(Node_number(token))

        elif token.type == TK_LPAREN:
            result.check(self.advance())
            expr = result.check(self.expr())
            if result.error: return result
            if self.current_token.type == TK_RPAREN:
                result.check(self.advance())
                return result.check_pass(expr)
            else: 
                return result.check_fail(InvalidSyntax(
                    self.current_token.initial_pos, self.current_token.final_pos,
                    "Expected ')' in -> "
                ))

        return result.check_fail(InvalidSyntax(
            token.initial_pos, token.final_pos,
            "Expected INT or FLOAT in -> "
        ))

    def term(self):
        return self.bin_operator(self.factor, (TK_MUL, TK_DIV))

    def expr(self):
        return self.bin_operator(self.term, (TK_PLUS, TK_MINUS))

    def bin_operator(self, function, operators):
        result = ParserChecker()
        left_side = result.check(function())
        if result.error: return result

        while self.current_token.type in operators:
            operation_token = self.current_token
            result.check(self.advance())
            right_side = result.check(function())
            if result.error: return result
            left_side = Node_Binary_op(left_side,operation_token, right_side)
        return result.check_pass(left_side)

