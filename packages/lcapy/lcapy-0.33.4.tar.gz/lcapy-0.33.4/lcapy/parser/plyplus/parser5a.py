from plyplus import Grammar

# @ at start of rule says to expand it
# # at start of rule says to flatten it
# ? at start of rule says to expand it if has one child

# The first two of the following work but not the third!

grammar1 = r"""
start: cpt whitespace node whitespace node whitespace value;
cpt: cpt_type cpt_id;
cpt_type: 'V' | 'R';
cpt_id: integer; 
integer: '\d+';
node: integer;
value: integer | name;
whitespace: '\s+';
"""

grammar2 = r"""
start: cpt whitespace node whitespace node whitespace value;
cpt: cpt_type cpt_id;
cpt_type: 'V' | 'R';
cpt_id: integer; 
integer: '\d+';
node: integer;
value: integer | name;
whitespace: '\s+';
name: '[a-z]+';
"""

grammar3 = r"""
start: cpt whitespace node whitespace node whitespace value;
cpt: cpt_type cpt_id;
cpt_type: 'V' | 'R';
cpt_id: integer; 
integer: '\d+';
node: integer;
value: integer | name;
whitespace: '\s+';
name: '\w+';
"""


import pdb
pdb.set_trace()
parser = Grammar(grammar2)

r = parser.parse('V1 2 3 4')
print(r)

r = parser.parse('V1 2 3 bert')
print(r)

