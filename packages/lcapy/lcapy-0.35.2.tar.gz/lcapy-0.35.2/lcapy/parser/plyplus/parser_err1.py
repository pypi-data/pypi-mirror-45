from plyplus import Grammar
from grammar import grammar

parser = Grammar(grammar)


r = parser.parse('R1 2')
print(r)
