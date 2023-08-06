from sympy import Symbol, ask, Q, exp, pi, I
from sympy.assumptions.assume import global_assumptions

x1 = Symbol('x')
x2 = Symbol('x', real=True)
x3 = Symbol('x')

y1 = 3 * x1 + 2
y2 = 3 * x2 + 2
y3 = 3 * x3 + 2

print(x1.is_real)
print(x2.is_real)

print(id(x1) == id(x3))

global_assumptions.add(Q.real(x3))


print(x1.is_real)
print(x3.is_real)

print(Q.real(x3) in global_assumptions)
print(ask(Q.real(x1)))
print(ask(Q.real(x2)))
print(ask(Q.real(x3)))

print(Q.real(y3) in global_assumptions)
print(ask(Q.real(y1)))
print(ask(Q.real(y2)))
print(ask(Q.real(y3)))

z1 = exp(2 * pi * I * x1)
# This uses the global assumptions.
print(z1.refine())

#global_assumptions.add(Q.integer(x1))
print(z1.refine())

facts = Q.integer(x1) & Q.positive(x1)
print(z1.refine(facts))
