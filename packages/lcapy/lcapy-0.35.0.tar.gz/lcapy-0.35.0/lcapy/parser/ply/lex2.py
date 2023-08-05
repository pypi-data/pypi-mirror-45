import ply.lex as lex

# List of token names.   This is always required
tokens = (
   'NUMBER',
   'NAME',
   'R',
   'V',
)

# Regular expression rules for simple tokens
t_R = r'^R'
t_V = r'^V'
t_NAME = r'(?<!^)\w+'


# Define as function so trumps NAME
def t_NUMBER(t):
    r'\d+'
    return t

# A string containing ignored characters
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
