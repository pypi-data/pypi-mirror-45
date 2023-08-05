from plyplus import Grammar
from grammar2 import grammar

parser = Grammar(grammar)

r = parser.parse('R1 2 3 4')
print(r)

r.to_png_with_pydot('foo.png')

r1 = parser.parse('R1 2 3')
print(r1)

q = parser.parse('Q1 2 3 4 pnp')
print(q)

j = parser.parse('Ja2 2 3 4 pjf')
print(j)

s = parser.parse('SW1 2 3 push')
print(s)

d = parser.parse('D1 2 3 led')
print(d)

v1 = parser.parse('V1 2 3')
print(v1)

v1 = parser.parse('V1 2 3 dc=4')
print(v1)

v2 = parser.parse('V1 2 3 ac 10, 20')
print(v2)

v3 = parser.parse('V1 2 3 sin(0 10 1000)')
print(v3)

v4 = parser.parse('V1 2 3 1.0e3')
print(v4)

v5 = parser.parse('V1 2 3 1e3')
print(v5)

r2 = parser.parse('R1 2 3 {5 * a}')
print(r2)
