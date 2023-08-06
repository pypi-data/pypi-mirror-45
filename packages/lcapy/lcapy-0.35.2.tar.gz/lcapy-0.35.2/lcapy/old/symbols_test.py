import sympy as sym

print(sym.Symbol('A', real=True).assumptions0)
print(sym.sympify('A').assumptions0)

