from YTechCode_lexer import *
from YTechCode_parser import *
import os
import math
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
    

Number.null = Number(0)
Number.false = Number(0)
Number.true = Number(1)
Number.pi = Number(math.pi)
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
    
    def __str__(self):
        return self.value

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
        copy = List(self.list_elements)
        copy.position(self.initial_pos, self.final_pos)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return ", ".join([str(x) for x in self.list_elements])

    def __repr__(self):
        return f'[{", ".join([str(x) for x in self.list_elements])}]'


################ BASE CLASE FOR FUNCTIONS ##########
class BaseFunction(Value):
    def __init__(self, func_name):
        super().__init__()
        self.func_name = func_name or "<nonamed>"

    def generate_context(self):
        function_context = Context(self.func_name, self.context, self.initial_pos)
        function_context.symbol_table = SymbolTable(function_context.context_parent.symbol_table)
        return function_context
    
    def check_arguments(self, arguments_names, arguments):
        checker = RunTimeChecker()
        if len(arguments) > len(arguments_names):
            return checker.check_fail(RunTimeError(
                self.initial_pos, self.final_pos, 
                f"{len(arguments) - len(arguments_names)} exceeded number of arguments in '{self.func_name}'", 
                self.context
            ))
        if len(arguments) < len(arguments_names):
            return checker.check_fail(RunTimeError(
                self.initial_pos, self.final_pos, 
                f"{ len(arguments_names) - len(arguments)} lack of parameters in '{self.func_name}'", 
                self.context
            ))
        return checker.check_pass(None)

    def fill_args(self, arguments_names, arguments, exec_context):
        for i in range(len(arguments)):
            argument_name = arguments_names[i]
            argument_value = arguments[i]
            argument_value.set_context(exec_context)
            exec_context.symbol_table.set(argument_name, argument_value)

    def check_and_fill_args(self, arguments_names, arguments, exec_context):
        checker = RunTimeChecker()
        checker.check(self.check_arguments(arguments_names, arguments))
        if checker.error: return checker
        self.fill_args(arguments_names, arguments, exec_context)
        return checker.check_pass(None)

################ FUNCTION CLASS ################
class Function(BaseFunction):
    def __init__(self, func_name, node_body, arguments_names):
        super().__init__(func_name)
        self.node_body = node_body
        self.arguments_names = arguments_names

    def execute(self, arguments):
        checker = RunTimeChecker()
        interpreter = Interpreter() 
        function_context = self.generate_context()

        checker.check(self.check_and_fill_args(self.arguments_names, arguments, function_context))
        if checker.error: return checker

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

############### BUILT-IN FUNCTION CLASS ##########
class BuiltInFunction(BaseFunction):
    def __init__(self, func_name):
        super().__init__(func_name)

    def execute(self, arguments):
        checker = RunTimeChecker()
        function_context = self.generate_context()

        method_name = f'execute_{self.func_name}'
        method = getattr(self, method_name, self.no_visit_method)

        checker.check(self.check_and_fill_args(method.arguments_names, arguments, function_context))
        if checker.error: return checker

        value = checker.check(method(function_context))
        if checker.error: return checker

        return checker.check_pass(value)


    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.func_name} method defined!')


    def copy(self):
        copy = BuiltInFunction(self.func_name)
        copy.set_context(self.context)
        copy.position(self.initial_pos, self.final_pos)
        return copy

    def __repr__(self):
        return f"<Built-in function {self.func_name}>"

    ############### DEFINITION OF THE BUILT-IN FUNCTIONS ####################333

    def execute_print(self, function_context):
        print(str(function_context.symbol_table.get('value')))
        return RunTimeChecker().check_pass(Number.null)
    execute_print.arguments_names = ['value']

    def execute_input(self, function_context):
        text = input()
        return RunTimeChecker().check_pass(String(text))
    execute_input.arguments_names = []

    def execute_number(self, function_context):
        text = str(function_context.symbol_table.get('value'))
        try:
            number = int(text)
        except ValueError:
            print(f"'{text}' not valid for conversion to number!")
        return RunTimeChecker().check_pass(Number(text))
    execute_number.arguments_names = ['value']

    def execute_string(self, function_context):
        text = (function_context.symbol_table.get('value'))
        if not isinstance(text, BaseFunction):
            return RunTimeChecker().check_pass(String(str(text)))
        else:
            return RunTimeChecker().check_fail(RunTimeError(
                self.initial_pos, self.final_pos,
                'Cannot convert functions into strings',
                function_context
            ))
    execute_string.arguments_names = ['value']

    def execute_len(self, function_context):
        text = function_context.symbol_table.get('value')
        if isinstance(text, String):
            text_len = len(str(text))
            return RunTimeChecker().check_pass(Number(text_len))
        elif isinstance(text, Number):
            text_len = len(str(text))
            return RunTimeChecker().check_pass(Number(text_len))
        elif isinstance(text, List):
            text_len = len(text.list_elements)
            return RunTimeChecker().check_pass(Number(text_len))
        else:
            return RunTimeChecker().check_fail(RunTimeError(
                self.initial_pos, self.final_pos,
                'Class <function> has not length',
                function_context
            ))
    execute_len.arguments_names = ['value']

    def execute_range(self, function_context):
        number = str(function_context.symbol_table.get('value'))
        try:
            number = int(number)
        except ValueError:
            print(f"'{number}' not valid for number")
        number_range = range(number)
        return RunTimeChecker().check_pass(List(number_range))
    execute_range.arguments_names = ['value']


    def execute_clear(self, function_context):
        os.system('cls' if os.name == "nt" else 'clear')
        return RunTimeChecker().check_pass(Number.null)
    execute_clear.arguments_names = []

    def execute_typeof(self, function_context):
        text = function_context.symbol_table.get('value')
        if isinstance(text, Number):
            text_type = "<class: Number>"
        elif isinstance(text, String):
            text_type = "<class: String>"
        elif isinstance(text, List):
            text_type = "<class: List>"
        elif isinstance(text, Function):
            text_type = "<class: Function>"
        return RunTimeChecker().check_pass(String(text_type))
    execute_typeof.arguments_names = ['value']

    def execute_is_number(self, function_context):
        is_number = isinstance(function_context.symbol_table.get("value"), Number)
        return RunTimeChecker().check_pass(Number.true if is_number else Number.false)
    execute_is_number.arguments_names = ['value']

    def execute_is_string(self, function_context):
        is_number = isinstance(function_context.symbol_table.get("value"), String)
        return RunTimeChecker().check_pass(Number.true if is_number else Number.false)
    execute_is_string.arguments_names = ['value']

    def execute_is_list(self, function_context):
        is_number = isinstance(function_context.symbol_table.get("value"), List)
        return RunTimeChecker().check_pass(Number.true if is_number else Number.false)
    execute_is_list.arguments_names = ['value']

    def execute_is_function(self, function_context):
        is_number = isinstance(function_context.symbol_table.get("value"), BaseFunction)
        return RunTimeChecker().check_pass(Number.true if is_number else Number.false)
    execute_is_function.arguments_names = ['value']

    def execute_append(self, function_context):
        list = function_context.symbol_table.get("list")
        value = function_context.symbol_table.get("value")

        if not isinstance(list, List):
            return RunTimeChecker.check_fail(RunTimeError(
                self.initial_pos, self.final_pos,
                "First argument must be a list!",
                function_context
            ))
        list.list_elements.append(value)
        return RunTimeChecker().check_pass(Number.null)
    execute_append.arguments_names = ['list', 'value']

    def execute_pop(self, function_context):
        list = function_context.symbol_table.get("list")
        index = function_context.symbol_table.get("index")

        if not isinstance(list, List):
            return RunTimeChecker.check_fail(RunTimeError(
                self.initial_pos, self.final_pos,
                "First argument must be a list!",
                function_context
            ))
        
        if not isinstance(index, Number):
            return RunTimeChecker.check_fail(RunTimeError(
                self.initial_pos, self.final_pos,
                "First argument must be a number!",
                function_context
            ))
        try:
            element = list.list_elements.pop(index.value)
        except:
            return RunTimeChecker().check_fail(RunTimeError(
                self.initial_pos, self.final_pos,
                'Element at this index could not be removed <Index out of bounds>',
                function_context
            ))
        return RunTimeChecker().check_pass(element)
    execute_pop.arguments_names = ['list', 'index']

    def execute_extend(self, function_context):
        list_1 = function_context.symbol_table.get("list_1")
        list_2 = function_context.symbol_table.get("list_2")

        if not isinstance(list_1, List):
            return RunTimeChecker().check_fail(RunTimeError(
                self.initial_pos, self.final_pos,
                "First argument must be a list!",
                function_context
            ))
        if not isinstance(list_2, List):
            return RunTimeChecker().check_fail(RunTimeError(
                self.initial_pos, self.final_pos,
                "Second argument must be a list!",
                function_context
            ))

        list_1.list_elements.extend(list_2.list_elements)
        return RunTimeChecker().check_pass(Number.null)
    execute_extend.arguments_names = ["list_1", "list_2"]

BuiltInFunction.print         = BuiltInFunction("print")  
BuiltInFunction.input         = BuiltInFunction("input")
BuiltInFunction.number        = BuiltInFunction("number")  
BuiltInFunction.string        = BuiltInFunction("string")  
BuiltInFunction.clear         = BuiltInFunction("clear")
BuiltInFunction.typeof        = BuiltInFunction("typeof")  
BuiltInFunction.is_number     = BuiltInFunction("is_number")
BuiltInFunction.is_string     = BuiltInFunction("is_string")  
BuiltInFunction.is_list       = BuiltInFunction("is_list")
BuiltInFunction.is_function   = BuiltInFunction("is_function")  
BuiltInFunction.len           = BuiltInFunction("len")  
BuiltInFunction.range         = BuiltInFunction("range")  
BuiltInFunction.append        = BuiltInFunction("append")
BuiltInFunction.pop           = BuiltInFunction("pop")  
BuiltInFunction.extend        = BuiltInFunction("extend")

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
        value = value.copy().position(node.initial_pos, node.final_pos).set_context(context)
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

        return_val = return_val.copy().position(node.initial_pos, node.final_pos).set_context(context)

        return checker.check_pass(return_val)



########### TEMPORAL RUN ##################
global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number.null)
global_symbol_table.set("NULL", Number.null)
global_symbol_table.set("false", Number.false)
global_symbol_table.set("FALSE", Number.false)
global_symbol_table.set("true", Number.true)
global_symbol_table.set("TRUE", Number.true)
global_symbol_table.set("PI", Number.pi)
global_symbol_table.set("print", BuiltInFunction.print)
global_symbol_table.set("input", BuiltInFunction.input)
global_symbol_table.set("number", BuiltInFunction.number)
global_symbol_table.set("string", BuiltInFunction.string)
global_symbol_table.set("clear", BuiltInFunction.clear)
global_symbol_table.set("typeof", BuiltInFunction.typeof)
global_symbol_table.set("is_number", BuiltInFunction.is_number)
global_symbol_table.set("is_string", BuiltInFunction.is_string)
global_symbol_table.set("is_list", BuiltInFunction.is_list)
global_symbol_table.set("is_function", BuiltInFunction.is_function)
global_symbol_table.set("len", BuiltInFunction.len)
global_symbol_table.set("range", BuiltInFunction.range)
global_symbol_table.set("append", BuiltInFunction.append)
global_symbol_table.set("pop", BuiltInFunction.pop)
global_symbol_table.set("extend", BuiltInFunction.extend)


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