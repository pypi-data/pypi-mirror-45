"""
This module provides the core functions and classes for Lcapy.

To print the rational functions in canonical form (with the highest
power of s in the denominator with a unity coefficient), use
print(x.canonical()).

For additional documentation, see the Lcapy tutorial.

Copyright 2014--2019 Michael Hayes, UCECE
"""




# Note imports at bottom to avoid circular dependencies



__all__ = ('pprint', 'pretty', 'latex', 'DeltaWye', 'WyeDelta', 'tf',
           'symbol', 'sympify',
           'zp2tf', 'Expr', 's', 'sExpr', 't', 'tExpr', 'f', 'fExpr', 'cExpr',
           'omega', 'omegaExpr', 
           'pi', 'cos', 'sin', 'tan', 'atan', 'atan2',
           'exp', 'sqrt', 'log', 'log10', 'gcd', 'oo', 'inf',
           'H', 'Heaviside', 'DiracDelta', 'j', 'u', 'delta',
           'Vector', 'Matrix', 'VsVector', 'IsVector', 'YsVector', 'ZsVector',
           'Hs', 'Is', 'Vs', 'Ys', 'Zs',
           'Hf', 'If', 'Vf', 'Yf', 'Zf',
           'In', 'Vn',

           'Isuper', 'Vsuper',
           'Homega', 'Iomega', 'Vomega', 'Yomega', 'Zomega')


