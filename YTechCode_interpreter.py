from YTechCode_lexer import *
from YTechCode_parser import *

############### RUN TIME CHECKER ##############

class RunTimeChecker:
    def __init__(self):
        self.value = None
        self.error = None
    
    def check(self, result):
        if result.error: self.error = result.error
        return result.value

    def check_pass(self, value):
        self.value = value
        return self

    def check_fail(self, error):
        self.error = error
        return self
############### CALCULATION LOGIC #############

class Number:
    def __init__(self, value):
        self.value = value
        self.position()
        self.set_context()

    def position(self, initial_pos = None, final_pos= None):
        self.initial_pos = initial_pos
        self.final_pos = final_pos
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def add_to(self, another_number):
        if isinstance(another_number, Number):
            return Number(self.value + another_number.value).set_context(self.context), None

    def sub_by(self, another_number):
        if isinstance(another_number, Number):
            return Number(self.value - another_number.value).set_context(self.context), None
    
    def mul_by(self, another_number):
        if isinstance(another_number, Number):
            return Number(self.value * another_number.value).set_context(self.context), None

    def div_by(self, another_number):
        if isinstance(another_number, Number):
            if another_number.value == 0:
                return None, RunTimeError(
                    another_number.initial_pos, another_number.final_pos,
                    'Division by zero!', self.context
                )
            return Number(self.value / another_number.value).set_context(self.context), None
    
    def pow_by(self, another_number):
        if isinstance(another_number, Number):
            return Number(self.value ** another_number.value).set_context(self.context), None

    def comparison_equal(self, another_number):
        if isinstance(another_number, Number):
            return Number(int(self.value == another_number.value)).set_context(self.context), None
    
    def comparison_notequal(self, another_number):
        if isinstance(another_number, Number):
            return Number(int(self.value != another_number.value)).set_context(self.context), None
    
    def comparison_less(self, another_number):
        if isinstance(another_number, Number):
            return Number(int(self.value < another_number.value)).set_context(self.context), None

    def comparison_greater(self, another_number):
        if isinstance(another_number, Number):
            return Number(int(self.value > another_number.value)).set_context(self.context), None
    
    def comparison_leq(self, another_number):
        if isinstance(another_number, Number):
            return Number(int(self.value <= another_number.value)).set_context(self.context), None
    
    def comparison_geq(self, another_number):
        if isinstance(another_number, Number):
            return Number(int(self.value >= another_number.value)).set_context(self.context), None

    def and_by(self, another_number):
        if isinstance(another_number, Number):
            return Number(int(self.value and another_number.value)).set_context(self.context), None

    def or_by(self, another_number):
        if isinstance(another_number, Number):
            return Number(int(self.value or another_number.value)).set_context(self.context), None

    def get_not(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None
    
    def copy(self):
        copy = Number(self.value)
        copy.position(self.initial_pos, self.final_pos)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0
    
    def __repr__(self):
        return str(self.value)


############## CONTEXT ########################
		
class Context:
	def __init__(self, context_name, context_parent=None, context_parent_entry_pos=None):
		self.context_name = context_name
		self.context_parent = context_parent
		self.context_parent_entry_pos = context_parent_entry_pos
		self.symbol_table = None

############### SYMBOL TABLE ##################

class SymbolTable:
    def __init__(self):
        self.symbols ={}
        self.parent = None
    
    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value
    
    def set(self, name, value):
        self.symbols[name] = value
    
    def remove(self, name):
        del self.symbols[name]

############## INTERPRETER ###################
class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method available')
    
    ####### Visit Methods ##########

    def visit_Node_number(self, node, context):
        checker = RunTimeChecker()
        return checker.check_pass(
            Number(node.token.value).set_context(context).position(node.initial_pos, node.final_pos)
            )

    def visit_Node_VarDeclare(self, node, context):
        checker = RunTimeChecker()
        variable_name= node.variable_name_token.value
        value = context.symbol_table.get(variable_name)

        if not value:
            return checker.check_fail(RunTimeError(
                node.initial_pos, node.final_pos,
                f"'{variable_name}' is not defined! ", context
            ))
        value = value.copy().position(node.initial_pos, node.final_pos)
        return checker.check_pass(value)
    
    def visit_Node_VarAssign(self, node, context):
        checker = RunTimeChecker()
        variable_name= node.variable_name_token.value
        value =  checker.check(self.visit(node.value_node, context))
        if checker.error: return checker

        context.symbol_table.set(variable_name, value)
        return checker.check_pass(value)

    def visit_Node_Binary_op(self, node, context):
        checker = RunTimeChecker()

        left = checker.check(self.visit(node.left_node, context))
        if checker.error: return checker
        right = checker.check(self.visit(node.right_node, context))
        if checker.error: return checker

        if node.operator_token.type == TK_PLUS:
            result, error = left.add_to(right)
        elif node.operator_token.type == TK_MINUS:
            result, error = left.sub_by(right)
        elif node.operator_token.type == TK_MUL:
            result, error = left.mul_by(right)
        elif node.operator_token.type == TK_DIV:
            result, error = left.div_by(right)
        elif node.operator_token.type == TK_POW:
            result, error = left.pow_by(right)
        elif node.operator_token.type == TK_DEQ:
            result, error = left.comparison_equal(right)
        elif node.operator_token.type == TK_NDEQ:
            result, error = left.comparison_notequal(right)
        elif node.operator_token.type == TK_LL:
            result, error = left.comparison_less(right)
        elif node.operator_token.type == TK_GG:
            result, error = left.comparison_greater(right)
        elif node.operator_token.type == TK_LEQ:
            result, error = left.comparison_leq(right)
        elif node.operator_token.type == TK_GEQ:
            result, error = left.comparison_geq(right)
        elif (node.operator_token.matches(TK_KEYWORD, 'AND')) or (node.operator_token.matches(TK_KEYWORD, 'and')):
            result, error = left.and_by(right)
        elif (node.operator_token.matches(TK_KEYWORD, 'OR')) or (node.operator_token.matches(TK_KEYWORD, 'or')):
            result, error = left.or_by(right)

        if error: 
            return checker.check_fail(error)
        else:
            return checker.check_pass(result.position(node.initial_pos, node.final_pos))

    def visit_Node_Unitary_op(self, node, context):
        checker = RunTimeChecker()
        
        number = checker.check(self.visit(node.node, context))
        if checker.error: return checker

        error = None

        if node.operator_token.type == TK_MINUS:
            number, error = number.mul_by(Number(-1))
        elif (self.operator_token.matches(TK_KEYWORD, 'NOT')) or (self.operator_token.matches(TK_KEYWORD, 'not')):
            number, error = number.get_not()
        
        if error: 
            return checker.check_fail(error)
        else:
            return checker.check_pass(number.position(node.initial_pos, node.final_pos))

    def visit_Node_If(self, node, context):
        checker = RunTimeChecker()

        for initial_cond, expr in node.if_elifs:
            initial_cond_value = checker.check(self.visit(initial_cond, context))
            if checker.error: return checker
            
            if initial_cond_value.is_true():
                expr_value = checker.check(self.visit(expr, context))
                if checker.error: return checker
                return checker.check_pass(expr_value)
            
        if node.else_case: 
            else_value = checker.check(self.visit(node.else_case, context))
            if checker.error: return checker
            return checker.check_pass(else_value)
        
        return checker.check_pass(None)

    def visit_Node_For(self, node, context):
        checker = RunTimeChecker()

        start_value = checker.check(self.visit(node.node_start_value, context))
        if checker.error: return checker

        final_value = checker.check(self.visit(node.node_final_value, context))
        if checker.error: return checker

        if node.node_step_value: 
            step_value = checker.check(self.visit(node.node_step_value, context))
            if checker.error: return checker
        else:
            step_value = Number(1)
        
        iter = start_value.value

        if step_value.value >= 0:
            condition = lambda: iter < final_value.value
        else:
            condition = lambda: iter > final_value.value
        
        while condition():
            context.symbol_table.set(node.variable_name_token.value, Number(iter))
            iter += step_value.value

            checker.check(self.visit(node.node_body, context))
            if checker.error: return checker
        
        return checker.check_pass(None)
    
    def visit_Node_While(self, node, context):
        checker = RunTimeChecker()
        while True:
            condition = checker.check(self.visit(node.node_condition, context))
            if checker.error: return checker

            if not condition.is_true(): break

            checker.check(self.visit(node.node_body, context))
            if checker.error: return checker
        
        return checker.check_pass(None)


### TEMPORAL RUN ###
global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))
global_symbol_table.set("NULL", Number(0))
global_symbol_table.set("false", Number(0))
global_symbol_table.set("FALSE", Number(0))
global_symbol_table.set("true", Number(1))
global_symbol_table.set("TRUE", Number(1))


def run(filename, string):
    lexer = Lexer(filename, string)
    tokens, error = lexer.create_tokens()
    if error: return None, error
    ## Parsing##
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error
    ## Executing ptogram ##
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error