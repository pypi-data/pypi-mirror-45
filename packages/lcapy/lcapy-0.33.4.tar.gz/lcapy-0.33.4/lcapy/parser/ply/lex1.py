import ply.lex as lex

# List of token names.   This is always required
tokens = (
    'INT',
    'FLOAT',
    'SEP',
    'NAME',
)

# Regular expression rules for simple tokens
t_SEP = r'\s+'

# If add other multiple letter names then modify t_CPT
cptnames = ('C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'O', 'Q', 'R', 'SW', 'TF', 'TP', 'V', 'W')
keywords = ('SIN', 'AC', 'DC')
reserved = keywords + cptnames
tokens += reserved


def t_FLOAT(t):
    r'[+-]?(([1-9][0-9]*\.[0-9]*)|(\.[0-9]+))([Ee][+-]?[0-9]+)?'
    return t

# Define as function so trumps NAME
def t_INT(t):
    r'\d+'
    return t

def t_CPT(t):
    r'^(SW|TF|TP|[A-Z])'
    t.type = t.value
    return t

def t_NAME(t):
    r'(?<!^)\w+'
    k = t.value.upper()
    t.type = k if k in keywords else 'NAME'
    return t


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

def test():
    doit('V1 1 2 3 4')
    doit('Va 1 2 3 4')
    doit('V 1 2 3 4.5')
    doit('V 1 2 3 SIN 1 2 3')
    doit('V 1 2 3 DC 4')
    doit('V 1 2 3 +4.5')
    doit('V 1 2 3 -4.5')
    doit('SW1 1 2')
