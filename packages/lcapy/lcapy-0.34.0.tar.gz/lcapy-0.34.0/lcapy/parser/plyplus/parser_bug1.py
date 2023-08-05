from plyplus import Grammar

grammar3 = r"""
start: cpt;
cpt: cpt_type cpt_id;
cpt_type: 'V' | 'R';
cpt_id: '\d+';
// The following produces ParserError even though name rule unused
name: '\w+';
// The following works
// name: '[a-z]+';
"""

parser = Grammar(grammar3, debug=True)

r = parser.parse('V1')
print(r)

