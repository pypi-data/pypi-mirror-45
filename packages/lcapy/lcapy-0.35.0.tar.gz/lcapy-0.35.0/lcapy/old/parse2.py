from sympy.parsing.sympy_parser import parse_expr

# To remove E1, create global_dict and remove E1, etc.

global_dict = {}
exec('from sympy import *', global_dict)
global_dict.pop('E1')
# delta gets printed as DiracDelta; could override
global_dict['delta'] = global_dict['DiracDelta']
global_dict['step'] = global_dict['Heaviside']


def parse(string):

    return parse_expr(string, global_dict=global_dict)


s1 = parse('5 * E1 + a')
s2 = parse('5 * delta(t)')
# Fails since expects delta to be a function
#s3 = parse('5 * delta')
