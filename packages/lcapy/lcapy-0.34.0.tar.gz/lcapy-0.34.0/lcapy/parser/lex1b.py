import ply.lex as lex

# When building the master regular expression, rules are added in the
# following order:
#
#    All tokens defined by functions are added in the same order as
#    they appear in the lexer file.
#
#    Tokens defined by strings are added next by sorting them in order
#    of decreasing regular expression length (longer expressions are
#    added first).


# List of token names.   This is always required
tokens = (
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'WHITESPACE',
   'NAME',
   'KEYWORD',
)

# Regular expression rules for simple tokens
t_KEYWORD = r'^\w'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_WHITESPACE = r'\s+'
t_NAME = r'(?<!^)\w+'
t_NUMBER = r'\d+'

# A string containing ignored characters
t_ignore  = ''

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

def doit(data):

    print(data)
    lexer.input(data)

    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)

doit('V1 1 2 3 4')
doit('Va 1 2 3 4')
doit('V 1 2 3 4')
