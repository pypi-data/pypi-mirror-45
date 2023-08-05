"""
This module performs nodal analysis.

Copyright 2019 Michael Hayes, UCECE

"""

from .mnacpts import L, C, I, V
from .matrix import Matrix
from .smatrix import sMatrix
from .tmatrix import tMatrix
from .sym import sympify, ssym
import sympy as sym

__all__ = ('Nodal', )

# TODO
# 1. Use a better Matrix class that preserves the class of each
# element, where possible.

# Independent sources
# V1 1 0
# V1 1 0 {10 * u(t)}
# V1 1 0 ac 10
#
# In each case, we use v1(t) as the independent source when determing
# the A, B, C, D matrices.  We can then substitute the known value at
# the end.

def _hack_vars(exprs):
    """Substitute iCanon1(t) with iC(t) etc. provided
    there is no iCanon2(t)."""

    for m, expr in enumerate(exprs):
        for c in ('iV', 'iC', 'iL', 'vC'):
            sym1 = sympify(c + 'anon1(t)')
            sym2 = sympify(c + 'anon2(t)')            
            if expr.has(sym1) and not expr.has(sym2):
                expr = expr.subs(sym1, sympify(c + '(t)'))
                exprs[m] = expr
                

class Nodal(object):
    """This converts a circuit to nodal representation."""

    def __init__(self, cct):

        self.cct = cct

        for node in cct.node_list:
            if node == '0':
                continue
            
        
    
from .symbols import t, s
from .expr import ExprList
from .texpr import Vt, It, tExpr
from .sexpr import sExpr
