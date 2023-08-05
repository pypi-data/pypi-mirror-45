import ply.yacc as yacc
from lex1 import tokens

import sys
sys.path.append('../..')

import schemcpts as cpts

def make(*args):

    classname = args[0]
    try:
        newclass = getattr(self.cpts, classname)
    except:
        newclass = self.cpts.newclasses[classname]
        
    obj = newclass(name, args[1:])    
    return obj


def anon_cpt_gen():
    count = 1
    while True:
        yield '#%d' % count
        count += 1

anon_cpt_id = anon_cpt_gen()

# Define productions
def p_start(p):
    '''start : cl
             | r
             | vi
             | viac
             | vidc
             | visin
    '''
    p[0] = p[1]

def p_cl(p):
    '''cl : C optid node node optvalue optvalue
          | L optid node node optvalue optvalue'''
    p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_r(p):
    'r : R optid node node optvalue'
    p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_vi(p):
    '''vi : V optid node node optvalue
          | I optid node node optvalue'''
    p[0] = (p[1], p[2], p[3], p[4], p[5])

def p_vidc(p):
    '''vidc : V optid node node SEP DC optvalue
            | I optid node node SEP DC optvalue'''
    p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7])

def p_viac(p):
    '''viac : V optid node node SEP AC optvalue optvalue
            | I optid node node SEP AC optvalue optvalue'''
    p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[7])

def p_visin(p):
    '''visin : V optid node node SEP SIN value value value optvalue
             | I optid node node SEP SIN value value value optvalue'''
    p[0] = (p[1], p[2], p[3], p[4], p[5], p[6], p[8])


def p_node_id(p):
    'node : SEP id'
    p[0] = p[2]

def p_id_name(p):
    '''id : NAME
          | INT'''
    p[0] = p[1]

def p_optid_id(p):
    '''optid : id
             | empty'''
    if p[1] == '':
        p[0] = anon_cpt_id.next()
    else:
        p[0] = p[1]

def p_value(p):
    '''value : SEP INT
             | SEP FLOAT'''
    p[0] = p[2]

def p_optvalue_id(p):
    '''optvalue : value
                | empty'''
    p[0] = p[1]

def p_empty(p):
    'empty : '
    p[0] = ''

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
doit('Rin 2 3 4.5')
doit('V 1 2 SIN 1 2 3')
doit('V 1 2 DC 4')
