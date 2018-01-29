import string

symbols = {
    '=': 'equal',
    'and': 'all',
    '>': 'greater_than',
    'or': 'any',
    '<': 'less_than',
    'not': 'sub',
    '!=': 'different',
    'xor': 'only',
    '>=': 'greater_or_equal',
    '>>': 'shift_right',
    '<=': 'less_or_equal',
    '<<': 'shift_left',
    '+': 'sum',
    '..': 'gradient',
    '-': 'sub',
    'in': 'contains',
    '*': 'mol',
    '+-': 'about',
    '/': 'div',
    ':': 'set',
    '^': 'pow',
    '->': 'pipe',
    '<-': 'inverse_pipe',
    '%': 'mod',
    ',': 'to_list',
    }

unary_symbols = {'+', '-', 'with', 'as'}

square_brace_start = ('[',)

string_starts = ("'", '"')

variable_starts = string.ascii_letters

curly_braces_start = ('{',)

inline_comment_start = ('//',)

multiline_comment_start = ('/*',)

exa_start = ('#',)

round_braces_start = ('(',)

whitespaces = (' ', '\t', '\n',)

prevent_new_line = ('\\n',)

assignation = (':',)

number_starts = (tuple(string.digits) + 
                 tuple("." + digit for digit in string.digits))