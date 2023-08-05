from sympy import Symbol

x1 = Symbol('x')
x2 = Symbol('x', real=True)
x3 = Symbol('x', real=True)

y1 = x1 * 3
y2 = x2 * 3
y3 = x3 * 3

print(x1.assumptions0)
print(x2.assumptions0)

# y1 != y2  but y2 == y3
print(y1 == y2)
print(y1 == y3)

x1._assumptions.update(x2._assumptions)
x2._assumptions.update(x1._assumptions)

print(x1.assumptions0)
print(x2.assumptions0)

print(y1 == y2)
print(y1 == y3)
