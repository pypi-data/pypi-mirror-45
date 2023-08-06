from plyplus import Grammar


# The first two of the following work but not the third!

grammar1 = r"""
start: cpt whitespace node;
cpt: cpt_type cpt_id;
cpt_type: 'V' | 'R';
cpt_id: integer; 
integer: '\d+';
node: integer;
whitespace: '\s+';
"""

grammar2 = r"""
start: cpt whitespace node;
cpt: cpt_type cpt_id;
cpt_type: 'V' | 'R';
cpt_id: integer; 
integer: '\d+';
node: integer;
whitespace: '\s+';
name: '[a-z]+';
"""

grammar3 = r"""
start: cpt;
cpt: cpt_type cpt_id;
cpt_type: 'V' | 'R';
cpt_id: integer; 
integer: '\d+';
node: integer;
value: integer;
whitespace: '\s+';
name: '\\w+';
"""


list_parser = Grammar(grammar3)

r = list_parser.parse('V1')
print(r)

