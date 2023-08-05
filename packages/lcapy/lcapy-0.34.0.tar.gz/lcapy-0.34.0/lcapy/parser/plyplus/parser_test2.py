from plyplus import Grammar
from grammar1 import grammar

parser = Grammar(grammar)

r = parser.parse('R1 2 3 4')
print(r)

r.to_png_with_pydot('foo.png')

r1 = parser.parse('R1 2 3')
print(r1)

q1 = parser.parse('Q1 2 3 4 pnp')
print(q1)

q2 = parser.parse('Q2 2 3 4 npn')
print(q2)

q3 = parser.parse('Q3 2 3 4')
print(q3)

s = parser.parse('SW1 2 3 push')
print(s)

d = parser.parse('D1 2 3 led')
print(d)

