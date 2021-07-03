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
class Value:
    def __init__(self):
        self.position()
        self.set_context()

    def position(self, initial_pos = None, final_pos= None):
        self.initial_pos = initial_pos
        self.final_pos = final_pos
        return self

    def set_context(self, context=None):
        self.context = context
        return self
    
    def add_to(self, other):
        return None, self.illegal_operation(other)

    def sub_by(self, other):
        return None, self.illegal_operation(other)
    
    def mul_by(self, other):
        return None, self.illegal_operation(other)

    def div_by(self, other):
        return None, self.illegal_operation(other)
    
    def pow_by(self, other):
        return None, self.illegal_operation(other)

    def comparison_equal(self, other):
        return None, self.illegal_operation(other)
    
    def comparison_notequal(self, other):
        return None, self.illegal_operation(other)
    
    def comparison_less(self, other):
        return None, self.illegal_operation(other)

    def comparison_greater(self, other):
        return None, self.illegal_operation(other)
    
    def comparison_leq(self, other):
        return None, self.illegal_operation(other)
    
    def comparison_geq(self, other):
        return None, self.illegal_operation(other)

    def and_by(self, other):
        return None, self.illegal_operation(other)

    def or_by(self, other):
        return None, self.illegal_operation(other)

    def get_not(self, other):
        return None, self.illegal_operation(other)
    
    def concat(self, other):
        return None, self.illegal_operation(other)
    
    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False
    

    def execute(self):
        return RunTimeChecker().check_fail(self.illegal_operation())
    
    def illegal_operation(self, other=None):
        if not other: other = self
        return RunTimeError(
            self.initial_pos, other.final_pos, 
            'Illegal Operation', 
            self.context
        )

class Number(Value):
    
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def add_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other) 

    def sub_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def mul_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def div_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(
                    other.initial_pos, other.final_pos,
                    'Division by zero!', self.context
                )
            return Number(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def pow_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def comparison_equal(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def comparison_notequal(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def comparison_less(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def comparison_greater(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def comparison_leq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def comparison_geq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def and_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def or_by(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

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
    
################ STRING CLASS ##################
class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
        
    def add_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def mul_by(self, other):
        if isinstance(other, Number):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def comparison_equal(self, other):
        if isinstance(other, String):
            return Number(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def comparison_notequal(self, other):
        if isinstance(other, String):
            return Number(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    
    def comparison_less(self, other):
        if isinstance(other, String):
            return Number(int(len(self.value) < len(other.value))).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def comparison_greater(self, other):
        if isinstance(other, String):
            return Number(int(len(self.value) > len(other.value))).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
        
    def sub_by(self, other):
        if isinstance(other, String):
            if self.value == other.value or (len(self.value)!=(len(other.value))):
                return None, Value.illegal_operation(self, other)
            else:
                self_array = []
                other_array = []
                string_diff =[]
                separator = ''
                for letter in self.value:
                    self_array.append(letter)
                for letter in other.value:
                    other_array.append(letter)
                for i in range(len(self_array)):
                    if self_array[i] != other_array[i]:
                        string_diff.append(self_array[i])
                    else:
                        pass
                if len(string_diff)==0:
                    return None, Value.illegal_operation(self, other)
                else:
                    string_diff = separator.join(string_diff)
                    return String(string_diff).set_context(self.context), None
            
            
            
    def is_true(self):
        return len(self.value) > 0
    
    def copy(self):
        copy = String(self.value)
        copy.set_context(self.context)
        copy.position(self.initial_pos, self.final_pos)
        return copy
    
    def __repr__(self):
        return f'"{self.value}"'
    
    
################ LIST CLASS ####################
class List(Value):
    def __init__(self, list_elements):
        super().__init__()
        self.list_elements = list_elements
        
    def add_to(self, other):
        new_list = self.copy()
        new_list.list_elements.append(other)
        return new_list, None

    def sub_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.list_elements.pop(other.value)
                return new_list, None
            except:
                return None, RunTimeError(
                    other.initial_pos, other.final_pos, 
                    'Index out of bounds <<element not removed>>',
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)

    def concat(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.list_elements.extend(other.list_elements)
            return new_list, None
        else:
            return None, Value.illegal_operation(self, other)
        
    def div_by(self, other):
        if isinstance(other, Number):
            try:
                return self.list_elements[other.value], None
            except:
                return None, RunTimeError(
                    other.initial_pos, other.final_pos, 
                    'Index out of bounds <<element not retrieved>>',
                    self.context
                )
        else:
            return None, Value.illegal_operation(self, other)
        
    def copy(self):
        copy = List(self.list_elements[:])
        copy.position(self.initial_pos, self.final_pos)
        copy.set_context(self.context)
        return copy
    
    def __repr__(self):
        return f'[{", ".join([str(x) for x in self.list_elements])}]'

################ FUNCTION CLASS ################
class Function(Value):
    def __init__(self, func_name, node_body, arguments_names):
        super().__init__()
        self.func_name = func_name or "<nonamed>" #For future implementation of anonymous functions
        self.node_body = node_body
        self.arguments_names = arguments_names

    def execute(self, arguments):
        checker = RunTimeChecker()
        interpreter = Interpreter() 
        function_context = Context(self.func_name, self.context, self.initial_pos)
        function_context.symbol_table = SymbolTable(function_context.context_parent.symbol_table)

        if len(arguments) > len(self.arguments_names):
            return checker.check_fail(RunTimeError(
                self.initial_pos, self.final_pos, 
                f"{len(arguments) - len(self.arguments_names)} exceeded number of arguments in '{self.func_name}'", 
                self.context
            ))
        if len(arguments) < len(self.arguments_names):
            return checker.check_fail(RunTimeError(
                self.initial_pos, self.final_pos, 
                f"{ len(self.arguments_names) - len(arguments)} lack of parameters in '{self.func_name}'", 
                self.context
            ))

        for i in range(len(arguments)):
            argument_name = self.arguments_names[i]
            argument_value = arguments[i]
            argument_value.set_context(function_context)
            function_context.symbol_table.set(argument_name, argument_value)

        value = checker.check(interpreter.visit(self.node_body, function_context))
        if checker.error: return checker
        return checker.check_pass(value)

    def copy(self):
        copy = Function(self.func_name, self.node_body, self.arguments_names)
        copy.set_context(self.context)
        copy.position(self.initial_pos, self.final_pos)
        return copy

    def __repr__(self):
        return f"DEFINED: <function {self.func_name}>"

############## CONTEXT ########################
		
class Context:
	def __init__(self, context_name, context_parent=None, context_parent_entry_pos=None):
		self.context_name = context_name
		self.context_parent = context_parent
		self.context_parent_entry_pos = context_parent_entry_pos
		self.symbol_table = None

############### SYMBOL TABLE ##################

class SymbolTable:
    def __init__(self, parent = None):
        self.symbols ={}
        self.parent = parent
    
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
            Number(node.token.value).set_context(context).position(node.initial_pos, node.final_pos))

    def visit_Node_string(self, node, context):
        checker = RunTimeChecker()
        return checker.check_pass(
            String(node.token.value).set_context(context).position(node.initial_pos, node.final_pos))
        
    def visit_Node_list(self, node, context):
        checker = RunTimeChecker()
        list_elements =[]
        
        for element in node.node_elements:
            list_elements.append(checker.check(self.visit(element, context)))
            if checker.error: return checker
        
        return checker.check_pass(
            List(list_elements).set_context(context).position(node.initial_pos, node.final_pos)
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
        elif node.operator_token.type == TK_PIPE:
            result, error = left.concat(right)
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
        elif (node.operator_token.matches(TK_KEYWORD, 'NOT')) or (node.operator_token.matches(TK_KEYWORD, 'not')):
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
        list_elements = []
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

            list_elements.append(checker.check(self.visit(node.node_body, context)))
            if checker.error: return checker
        
        return checker.check_pass(
            List(list_elements).set_context(context).position(node.initial_pos, node.final_pos)
        )
    
    def visit_Node_While(self, node, context):
        checker = RunTimeChecker()
        list_elements = []
        while True:
            condition = checker.check(self.visit(node.node_condition, context))
            if checker.error: return checker

            if not condition.is_true(): break

            list_elements.append(checker.check(self.visit(node.node_body, context)))
            if checker.error: return checker
        
        return checker.check_pass(
            List(list_elements).set_context(context).position(node.initial_pos, node.final_pos)
        )

    def visit_Node_Def_function(self, node, context):
        checker = RunTimeChecker()

        function_name = node.variable_name_token.value if node.variable_name_token else None  ##Anonymous Functions
        body_node = node.node_body
        arguments_names = [arg_name.value for arg_name in node.arguments_token]
        function_value = Function(function_name, body_node, arguments_names).set_context(context).position(node.initial_pos, node.final_pos)

        if node.variable_name_token: #usefull when implementing anonymous functions
            context.symbol_table.set(function_name, function_value)
        return checker.check_pass(function_value)

    def visit_Node_call_func(self, node, context):
        checker = RunTimeChecker()
        arguments = []

        call_value = checker.check(self.visit(node.call_to_node, context))
        if checker.error: return checker
        call_value = call_value.copy().position(node.initial_pos, node.final_pos)

        for node_argument in node.node_args:
            arguments.append(checker.check(self.visit(node_argument, context)))
            if checker.error: return checker
        
        return_val = checker.check(call_value.execute(arguments))
        if checker.error: return checker

        return checker.check_pass(return_val)



########### TEMPORAL RUN ##################
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