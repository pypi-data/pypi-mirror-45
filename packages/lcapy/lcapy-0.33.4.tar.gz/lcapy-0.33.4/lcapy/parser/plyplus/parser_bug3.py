from plyplus import Grammar

grammar1 = r"""
start: thing sep xnode;
thing: (V | R);
//V: 'V' string;
//R: 'R' string;
V: 'V\d+';
R: 'R\d+';
integer: '\d+';
xnode: integer | string;
string: '\w+';
@sep: '\s+';
"""

parser = Grammar(grammar1, debug=True)

r = parser.parse('V1 a1')
print(r)

