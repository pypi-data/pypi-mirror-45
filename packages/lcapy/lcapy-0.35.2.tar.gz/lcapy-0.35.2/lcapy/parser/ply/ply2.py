import ply.yacc as yacc
from lex2 import tokens

# This version gobbles separators.


# Define productions
def p_start(p):
    '''start : Vexpr
             | Rexpr'''
    p[0] = p[1]

def p_Vexpr(p):
    'Vexpr : V optid node node optvalue'
    p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_Rexpr(p):
    'Rexpr : R optid node node optvalue'
    p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_node_id(p):
    'node : id'
    p[0] = p[1]

def p_id_name(p):
    'id : NAME'
    p[0] = p[1]

def p_optid_id(p):
    '''optid : id
             | empty'''
    p[0] = p[1]

def p_optvalue_id(p):
    '''optvalue : id
                | empty'''
    p[0] = p[1]

def p_empty(p):
    'empty : '
    p[0] = ''

def p_id_number(p):
    'id : NUMBER'
    p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error with token %s at column %s" % (p.type, p.lexpos))
#    print(vars(p))

# Build the parser
parser = yacc.yacc()

def doit(data):

    print(data)
    #result = parser.parse(data, debug=True)
    result = parser.parse(data)
    print(result)

doit('V1 1 2 3')
doit('Va 1 2 3')
doit('V 1 2 3')
doit('Rin 2 3 4')
