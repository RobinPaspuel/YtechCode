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
    
    def __repr__(self):
        return str(self.value)


############## CONTEXT ########################
		
class Context:
	def __init__(self, context_name, context_parent=None, context_parent_entry_pos=None):
		self.context_name = context_name
		self.context_parent = context_parent
		self.parent_entry_pos = context_parent_entry_pos
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

        if error: 
            return checker.check_fail(error)
        else:
            return checker.check_pass(number.position(node.initial_pos, node.final_pos))

### TEMPORAL RUN ###
global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))

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