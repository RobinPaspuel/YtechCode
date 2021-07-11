from YTechCode_lexer import *

##### DEFINING NODES ########

class Node_number:
    def __init__(self, token):
        self.token = token
        self.initial_pos = self.token.initial_pos
        self.final_pos = self.token.final_pos

    def __repr__(self):
        return f'{self.token}'
    
class Node_string:
    def __init__(self, token):
        self.token = token
        self.initial_pos = self.token.initial_pos
        self.final_pos = self.token.final_pos

    def __repr__(self):
        return f'{self.token}'

class Node_list:
    def __init__(self, node_elements, initial_pos, final_pos):
        self.node_elements = node_elements
        self.initial_pos = initial_pos
        self.final_pos = final_pos
        

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
        
    def __repr__(self):
        return f'VARIABLE: {self.variable_name_token.value}: {self.value_node}'

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

class Node_If:
    def __init__(self, if_elifs, else_case):
        self.if_elifs = if_elifs
        self.else_case = else_case

        self.initial_pos = self.if_elifs[0][0].initial_pos
        self.final_pos = (self.else_case or self.if_elifs[len(self.if_elifs)-1])[0].final_pos

    def __repr__(self):
        if len(self.if_elifs)==1:
            return f'CONDITIONAL: ({self.if_elifs}), ELSE: ({self.else_case})'
        else:
            return f'CONDITIONALS: ({self.if_elifs}), ELSE: ({self.else_case})'
class Node_For:
    def __init__(self, variable_name_token, node_start_value, node_final_value, node_step_value, node_body, return_null):
        self.variable_name_token = variable_name_token
        self.node_start_value = node_start_value
        self.node_final_value = node_final_value
        self.node_step_value = node_step_value
        self.node_body = node_body
        self.return_null = return_null

        self.initial_pos = self.variable_name_token.initial_pos
        self.final_pos = self.node_body.final_pos

    def __repr__(self):
        return f"LOOP: FOR ({self.variable_name_token} = {self.node_start_value} : {self.node_final_value} : {self.node_step_value}) {'{'} {self.node_body} {'}'}"

class Node_While:
    def __init__(self, node_condition, node_body, return_null):
        self.node_condition = node_condition
        self.node_body = node_body
        self.return_null = return_null

        self.initial_pos = self.node_condition.initial_pos
        self.final_pos = self.node_body.final_pos

    def __repr__(self):
        return f"LOOP: WHILE ({self.node_condition}) {'{'}{self.node_body} {'}'}"

class Node_Def_function:
    def __init__(self, variable_name_token, arguments_token, node_body, return_self_value):
        self.variable_name_token = variable_name_token
        self.arguments_token = arguments_token
        self.node_body = node_body
        self.return_self_value = return_self_value

        self.initial_pos = self.variable_name_token.initial_pos
        self.final_pos = self.node_body.final_pos

    def __repr__(self):
        return f'FUNCTION: {self.variable_name_token.value}'   
        
class Node_call_func:
    def __init__(self, call_to_node, node_args):
        self.call_to_node = call_to_node
        self.node_args = node_args

        self.initial_pos = self.call_to_node.initial_pos

        if len(self.node_args) > 0:
            self.final_pos = self.node_args[len(self.node_args) - 1].final_pos
        else:
            self.final_pos = self.call_to_node.final_pos

class Node_return:
    def __init__(self, return_node, initial_pos, final_pos):
        self.return_node = return_node

        self.initial_pos = initial_pos
        self.final_pos = final_pos

class Node_next:
    def __init__(self, initial_pos, final_pos):
        self.initial_pos = initial_pos
        self.final_pos = final_pos

class Node_break:
    def __init__(self, initial_pos, final_pos):
        self.initial_pos = initial_pos
        self.final_pos = final_pos

########## PARSER CHECKER ##############

class ParserChecker:
    def __init__(self):
        self.error = None
        self.node  = None
        self.advance_step = 0
        self.last_registered_advance_count = 0
        self.to_reverse_count = 0

    def check_advance(self):
        self.last_registered_advance_count = 1
        self.advance_step += 1


    def check(self, result):
        self.last_registered_advance_count = result.advance_step
        self.advance_step += result.advance_step
        if result.error: self.error = result.error
        return result.node
        
    def try_check(self, result):
        if result.error:
            self.to_reverse_count = result.advance_step
            return None
        return self.check(result)

    def check_pass(self, node):
        self.node = node
        return self

    def check_fail(self, error):
        if not self.error or self.last_registered_advance_count == 0:
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
        self.update_current_token()   
        return self.current_token

    def reverse(self, amount=1):
        self.token_index -= amount
        self.update_current_token()
        return self.current_token

    def update_current_token(self):
        if self.token_index >= 0 and self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]

    def parse(self):
        result = self.statements()
        if not result.error and self.current_token.type !=  TK_EOF:
            return result.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                f"Expected '+', '-', '*' or '/' in -> "
            ))
        return result

    def def_func(self):
        checker = ParserChecker()

        if not ((self.current_token.matches(TK_KEYWORD, 'DEF')) or (self.current_token.matches(TK_KEYWORD, 'def'))):
            return checker.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                f"Expected 'DEF' or 'def' in -> "
            ))
        checker.check_advance()
        self.advance()

        if self.current_token.type != TK_IDENTIFIER:
            return checker.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                f"Expected a function name in -> "
            ))

        variable_name = self.current_token
        checker.check_advance()
        self.advance()

        if self.current_token.type != TK_LPAREN:
            return checker.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                f"Expected '(' in -> "
            ))
        checker.check_advance()
        self.advance()
        arguments_token = []

        if self.current_token.type == TK_IDENTIFIER:
            arguments_token.append(self.current_token)
            checker.check_advance()
            self.advance()

            while self.current_token.type == TK_COMMA:
                checker.check_advance()
                self.advance()
                if self.current_token.type != TK_IDENTIFIER:
                    return checker.check_fail(InvalidSyntax(
                        self.current_token.initial_pos, self.current_token.final_pos,
                        f"Expected an additional parameter in -> "
                    ))
                arguments_token.append(self.current_token)
                checker.check_advance()
                self.advance()
            
            if self.current_token.type != TK_RPAREN:
                return checker.check_fail(InvalidSyntax(
                    self.current_token.initial_pos, self.current_token.final_pos,
                    f"Expected ',' or ')' in -> "
                ))
            
        
        else:
            if self.current_token.type != TK_RPAREN:
                return checker.check_fail(InvalidSyntax(
                    self.current_token.initial_pos, self.current_token.final_pos,
                    f"Expecet a parameter or ')' in -> "
                ))
        checker.check_advance()
        self.advance() 

        if self.current_token.type != TK_CBL:
            return checker.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                "Expected '{' in -> "
            ))
        checker.check_advance()
        self.advance()

        if self.current_token.type == TK_NLINE:
            checker.check_advance()
            self.advance()

            return_node = checker.check(self.statements())
            if checker.error: return checker

            if self.current_token.type != TK_CBR:
                return checker.check_fail(InvalidSyntax(
                    self.current_token.initial_pos, self.current_token.final_pos,
                    "Expected '}' in -> "
                ))
                
            checker.check_advance()
            self.advance()

            return checker.check_pass(Node_Def_function(variable_name, arguments_token, return_node, False))

        return_node = checker.check(self.expr())
        if checker.error: return checker

        if self.current_token.type != TK_CBR:
            return checker.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                "Expected '}' in -> "
            ))
        checker.check_advance()
        self.advance()

        return checker.check_pass(Node_Def_function(variable_name, arguments_token, return_node, True))
       

    def for_statement(self):
        checker = ParserChecker()

        if not ((self.current_token.matches(TK_KEYWORD, 'FOR')) or (self.current_token.matches(TK_KEYWORD, 'for'))):
            return checker.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                f"Expected 'FOR' or 'for' in -> "
            ))

        checker.check_advance()
        self.advance()

        if self.current_token.type != TK_IDENTIFIER:
            return checker.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                f"Expected a variable to iterate in -> "
            ))
        
        variable_name = self.current_token
        checker.check_advance()
        self.advance()

        if self.current_token.type != TK_EQUALS:
            return checker.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                f"Expected '=' in -> "
            ))
        
        checker.check_advance()
        self.advance()

        start_value = checker.check(self.expr())
        if checker.error: return checker

        if self.current_token.type != TK_COLON:
            return checker.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                f"Expected ':' in -> "
            ))
        
        checker.check_advance()
        self.advance()

        final_value = checker.check(self.expr())
        if checker.error: return checker

        if self.current_token.type == TK_COLON:
            checker.check_advance()
            self.advance()

            step_value = checker.check(self.expr())
            if checker.error: return checker
        else:
            step_value = None

        if self.current_token.type != TK_CBL:
            return checker.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                f"Expected {'{'} in -> "
            ))
        
        checker.check_advance()
        self.advance()

        if self.current_token.type == TK_NLINE:
            checker.check_advance()
            self.advance()

            body = checker.check(self.statements())
            if checker.error: return checker

            if self.current_token.type != TK_CBR:
                return checker.check_fail(InvalidSyntax(
                    self.current_token.initial_pos, self.current_token.final_pos,
                    f"Expected {'}'} in -> '"
                ))
            checker.check_advance()
            self.advance()
            
            return checker.check_pass(Node_For(variable_name, start_value, final_value, step_value, body, True))
        
        body = checker.check(self.statement())
        if checker.error: return checker

        if not self.current_token.type ==TK_CBR:
            return checker.check_fail(InvalidSyntax(
                    self.current_token.initial_pos, self.current_token.final_pos,
                    f"Expected {'}'} in -> '"
                ))
        checker.check_advance()
        self.advance()

        return checker.check_pass(Node_For(variable_name, start_value, final_value, step_value, body, False))

    def while_statement(self):
        checker = ParserChecker()

        if not ((self.current_token.matches(TK_KEYWORD, 'WHILE')) or (self.current_token.matches(TK_KEYWORD, 'while'))):
            return checker.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                f"Expected 'WHILE' or 'while' in -> "
            ))

        checker.check_advance()
        self.advance()

        node_condition = checker.check(self.expr())
        if checker.error: return checker

        if self.current_token.type != TK_CBL:
            return checker.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                f"Expected {'{'} in -> "
            ))
        checker.check_advance()
        self.advance()

        if self.current_token.type == TK_NLINE:
            checker.check_advance()
            self.advance()

            body = checker.check(self.statements())
            if checker.error: return checker

            if self.current_token.type != TK_CBR:
                return checker.check_fail(InvalidSyntax(
                    self.current_token.initial_pos, self.current_token.final_pos,
                    f"Expected {'}'} in -> "
                ))
            checker.check_advance()
            self.advance()
            return checker.check_pass(Node_While(node_condition, body, True))
        
        body = checker.check(self.statement())
        if checker.error: return checker

        if not self.current_token.type ==TK_CBR:
            return checker.check_fail(InvalidSyntax(
                    self.current_token.initial_pos, self.current_token.final_pos,
                    f"Expected {'}'} in -> '"
                ))
        checker.check_advance()
        self.advance()

        return checker.check_pass(Node_While(node_condition, body, False))

    def if_statement(self):
        checker = ParserChecker()
        all_cases = checker.check(self.if_stmt_cases('if'))
        if checker.error: return checker
        cases, else_case = all_cases
        return checker.check_pass(Node_If(cases, else_case))

    def elif_expr(self):
        return self.if_stmt_cases('elif')

    def else_expr(self):
        checker = ParserChecker()
        else_case = None

        if self.current_token.matches(TK_KEYWORD, 'else'):
            checker.check_advance()
            self.advance()

            if not self.current_token.type == TK_CBL:
                return checker.check_fail(InvalidSyntax(
                            self.current_token.initial_pos, self.current_token.final_pos,
                            f"Expected {'{'} in -> "
                        ))
            checker.check_advance()
            self.advance()

            if self.current_token.type == TK_NLINE:
                checker.check_advance()
                self.advance()

                statements = checker.check(self.statements())
                if checker.error: return checker
                else_case = (statements, True)

                if self.current_token.type== TK_CBR:
                    checker.check_advance()
                    self.advance()
                else:
                    return checker.check_fail(InvalidSyntax(
                        self.current_token.initial_pos, self.current_token.final_pos,
                        f"Expected {'}'} in -> "
                    ))
            else:
                
                expr = checker.check(self.statement())
                if checker.error: return checker
                else_case = (expr, False)

                if not self.current_token.type == TK_CBR:
                    return checker.check_fail(InvalidSyntax(
                        self.current_token.initial_pos, self.current_token.final_pos,
                        f"Expected {'}'} in -> "
                    ))
                checker.check_advance()
                self.advance()

        return checker.check_pass(else_case)

    def if_elif_or_else(self):
        checker=ParserChecker()
        cases, else_case = [], None

        if self.current_token.matches(TK_KEYWORD, 'elif'):
            all_cases = checker.check(self.elif_expr())
            if checker.error: return checker
            cases, else_case = all_cases
        else:
            else_case = checker.check(self.else_expr())
            if checker.error: return checker
    
        return checker.check_pass((cases, else_case))

    def if_stmt_cases(self, key_word):
        checker = ParserChecker()
        cases = []
        else_case = None

        if not ((self.current_token.matches(TK_KEYWORD, key_word))):
            return checker.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                f"Expected '{key_word}' in -> "
            ))
        checker.check_advance()
        self.advance()

        initial_cond = checker.check(self.expr())
        if checker.error: return checker

        if not self.current_token.type == TK_CBL:
            return checker.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                f"Expected {'{'} in -> "
            ))
        checker.check_advance()
        self.advance()

        if self.current_token.type == TK_NLINE:
            checker.check_advance()
            self.advance()

            statements = checker.check(self.statements())
            if checker.error: return checker
            cases.append((initial_cond, statements, True))

            if self.current_token.type == TK_CBR:
                checker.check_advance()
                self.advance()
            #else:
                
            all_cases = checker.check(self.if_elif_or_else())
            if checker.error: return checker
            new_cases, else_case = all_cases
            cases.extend(new_cases)


        else:
            expr = checker.check(self.statement())
            if checker.error: return checker
            cases.append((initial_cond, expr, False))

            if not self.current_token.type == TK_CBR:
                return checker.check_fail(InvalidSyntax(
                    self.current_token.initial_pos, self.current_token.final_pos,
                    f"Expected {'}'} in -> "
                ))
            checker.check_advance()
            self.advance()

            all_cases = checker.check(self.if_elif_or_else())
            if checker.error: return checker
            new_cases, else_case = all_cases
            cases.extend(new_cases)

        return checker.check_pass((cases, else_case))


    def list_stmt(self):
        checker = ParserChecker()
        node_elements = []
        initial_pos = self.current_token.initial_pos.copy()
        
        if self.current_token.type != TK_LSPAREN:
            return checker.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos, 
                f"Expected '[' in -> "
            ))
        checker.check_advance()
        self.advance()
        
        if self.current_token.type == TK_RSPAREN:
            checker.check_advance()
            self.advance()
        else:
            node_elements.append(checker.check(self.expr())) 
            if checker.error: 
                return checker.check_fail(InvalidSyntax(
                    self.current_token.initial_pos, self.current_token.final_pos,
                    f"Expected ']', 'LET or let', while-loop, for-loop, INT, FLOAT, IDENTIFIER in  -> "
                ))
            while self.current_token.type == TK_COMMA:
                checker.check_advance()
                self.advance()

                node_elements.append(checker.check(self.expr()))
                if checker.error: return checker
                
            if self.current_token.type != TK_RSPAREN:
                return checker.check_fail(InvalidSyntax(
                    self.current_token.initial_pos, self.current_token.final_pos,
                    f"Expected ',' or ']' in -> "
                ))
            checker.check_advance()
            self.advance()
        
        return checker.check_pass(Node_list(node_elements, initial_pos, self.current_token.final_pos.copy()))
            
        

    def atom(self):
        result = ParserChecker()
        token = self.current_token

        if token.type in (TK_INT, TK_FLOAT):
            result.check_advance()
            self.advance()
            return result.check_pass(Node_number(token))
        
        elif token.type == TK_STRING:
            result.check_advance()
            self.advance()
            return result.check_pass(Node_string(token))

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
                    f"Expected ')' in -> "
                ))
                
        elif token.type == TK_LSPAREN:
            list_stmt = result.check(self.list_stmt())
            if result.error: return result
            return result.check_pass(list_stmt)

        elif (token.matches(TK_KEYWORD, 'IF')) or (token.matches(TK_KEYWORD, 'if')):
            if_statement = result.check(self.if_statement())
            if result.error: return result
            return result.check_pass(if_statement)

        elif (token.matches(TK_KEYWORD, 'FOR')) or (token.matches(TK_KEYWORD, 'for')):
            for_statement = result.check(self.for_statement())
            if result.error: return result
            return result.check_pass(for_statement)

        elif (token.matches(TK_KEYWORD, 'WHILE')) or (token.matches(TK_KEYWORD, 'while')):
            while_statement = result.check(self.while_statement())
            if result.error: return result
            return result.check_pass(while_statement)

        elif (token.matches(TK_KEYWORD, 'DEF')) or (token.matches(TK_KEYWORD, 'def')):
            function_name = result.check(self.def_func())
            if result.error: return result
            return result.check_pass(function_name)

        return result.check_fail(InvalidSyntax(
            self.current_token.initial_pos, self.current_token.final_pos,
            f"Expected INT, FLOAT, IDENTIFIER,  '+', '-', '(', '[' , 'FOR', 'WHILE' or 'DEF' in -> "
        ))

    def call_func(self):
        checker = ParserChecker()
        atom = checker.check(self.atom())
        if checker.error: return checker
        
        if self.current_token.type == TK_LPAREN:
            checker.check_advance()
            self.advance()
            arguments_nodes = []

            if self.current_token.type == TK_RPAREN:
                checker.check_advance()
                self.advance()
            else:
                arguments_nodes.append(checker.check(self.expr())) 
                if checker.error: 
                    return checker.check_fail(InvalidSyntax(
                        self.current_token.initial_pos, self.current_token.final_pos,
                        f"Expected ')', 'LET or let', while-loop, for-loop, INT, FLOAT, IDENTIFIER in  -> "
                    ))
                while self.current_token.type == TK_COMMA:
                    checker.check_advance()
                    self.advance()

                    arguments_nodes.append(checker.check(self.expr()))
                    if checker.error: return checker
                
                if self.current_token.type != TK_RPAREN:
                    return checker.check_fail(InvalidSyntax(
                        self.current_token.initial_pos, self.current_token.final_pos,
                        f"Expected ')' in -> "
                    ))
                checker.check_advance()
                self.advance()
            return checker.check_pass(Node_call_func(atom, arguments_nodes))
        return checker.check_pass(atom)
    
    def power(self):
        return self.bin_operator(self.call_func, (TK_POW, ), self.factor)

    def factor(self):
        result = ParserChecker()
        token = self.current_token

        if token.type in (TK_PLUS, TK_MINUS, TK_PIPE):
            result.check_advance()
            self.advance()
            factor = result.check(self.factor())
            if result.error: return result
            return result.check_pass(Node_Unitary_op(token, factor))

        return self.power()
    

    def term(self):
        return self.bin_operator(self.factor, (TK_MUL, TK_DIV, TK_PIPE))

    def arith_expr(self):
        return self.bin_operator(self.term, (TK_PLUS, TK_MINUS))        

    def comparison_expr(self):
        checker = ParserChecker()

        if (self.current_token.matches(TK_KEYWORD, 'NOT')) or (self.current_token.matches(TK_KEYWORD, 'not')):
            relation_token = self.current_token
            checker.check_advance()
            self.advance()
            node = checker.check(self.comparison_expr())
            if checker.error: return checker
            return checker.check_pass(Node_Unitary_op(relation_token, node))
        node = checker.check(self.bin_operator(self.arith_expr, (TK_DEQ, TK_NDEQ, TK_LL, TK_GG, TK_LEQ, TK_GEQ)))
        if checker.error: 
            return checker.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                f"Expected INT, FLOAT, IDENTIFIER,  '+', '-', '(', '[' or 'NOT' in -> "
            ))
        return checker.check_pass(node)

    def expr(self):
        result = ParserChecker()
        if (self.current_token.matches(TK_KEYWORD, 'let')) or (self.current_token.matches(TK_KEYWORD, 'LET')):
            result.check_advance()
            self.advance()
            if self.current_token.type != TK_IDENTIFIER:
                return result.check_fail(InvalidSyntax(
                    self.current_token.initial_pos, self.current_token.final_pos,
                    f'Expected a valid variable name  in -> '
                ))
            variable_name = self.current_token
            result.check_advance()
            self.advance()
        
            if self.current_token.type != TK_EQUALS:
                return result.check_fail(InvalidSyntax(
                    self.current_token.initial_pos, self.current_token.final_pos,
                    f"Expected '=' in -> "
                ))
            result.check_advance()
            self.advance()
            expr = result.check(self.expr())
            if result.error: return result
            return result.check_pass(Node_VarAssign(variable_name, expr))

        node = result.check(self.bin_operator(self.comparison_expr, ((TK_KEYWORD, "AND"), (TK_KEYWORD, "OR"), 
                                                                    (TK_KEYWORD, "and"), (TK_KEYWORD, "or"))))
        if result.error: 
            return result.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                f"Expected 'LET or let', INT, FLOAT, IDENTIFIER, '+', '-', '(', or '[' in -> "
            ))
        return result.check_pass(node)

    def bin_operator(self, function_one, operators, function_two=None):
        if function_two == None:
            function_two = function_one
        result = ParserChecker()
        left_side = result.check(function_one())
        if result.error: return result

        while self.current_token.type in operators or (self.current_token.type, self.current_token.value) in operators:
            operation_token = self.current_token
            result.check_advance()
            self.advance()
            right_side = result.check(function_two())
            if result.error: return result
            left_side = Node_Binary_op(left_side,operation_token, right_side)
        return result.check_pass(left_side)

    def statement(self):
        checker = ParserChecker()
        initial_pos = self.current_token.initial_pos.copy()

        if self.current_token.matches(TK_KEYWORD, 'return'):
            checker.check_advance()
            self.advance()

            expr = checker.try_check(self.expr())
            if not expr:
                self.reverse(checker.to_reverse_count)
            return checker.check_pass(Node_return(expr, initial_pos, self.current_token.initial_pos.copy()))

        if self.current_token.matches(TK_KEYWORD, 'next'):
            checker.check_advance()
            self.advance()
            return checker.check_pass(Node_next(initial_pos, self.current_token.initial_pos.copy()))

        if self.current_token.matches(TK_KEYWORD, 'break'):
                    checker.check_advance()
                    self.advance()
                    return checker.check_pass(Node_break(initial_pos, self.current_token.initial_pos.copy()))

        expr = checker.check(self.expr())
        if checker.error: 
            return checker.check_fail(InvalidSyntax(
                self.current_token.initial_pos, self.current_token.final_pos,
                f"Expected 'return', 'continue', 'break', 'let', INT, FLOAT, IDENTIFIER, '+', '-', '(', or '[' in -> "
            ))

        return checker.check_pass(expr)

    def statements(self):
        checker = ParserChecker()
        statements = []
        initial_pos = self.current_token.initial_pos.copy()

        while self.current_token.type == TK_NLINE:
            checker.check_advance()
            self.advance()

        statement = checker.check(self.statement())
        if checker.error: return checker
        statements.append(statement)

        more_statemets = True

        while True:
            nlines_count = 0
            while self.current_token.type == TK_NLINE:
                checker.check_advance()
                self.advance()
                nlines_count += 1
            if nlines_count == 0:
                more_statemets = False

            if not more_statemets: break
            statement = checker.try_check(self.statement())
            if not statement:
                self.reverse(checker.to_reverse_count)
                more_statemets = False
                continue
            statements.append(statement)

        return checker.check_pass(Node_list(
            statements, initial_pos, self.current_token.final_pos.copy()
        ))


def parser_run(filename, text):
		# Generate tokens
		lexer = Lexer(filename, text)
		tokens, error = lexer.create_tokens()
		if error: return None, error
		
		# Generate AST
		parser = Parser(tokens)
		ast = parser.parse()

		return ast.node, ast.error