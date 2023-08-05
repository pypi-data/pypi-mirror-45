from plyplus import Grammar

# @ at start of rule says to expand it
# # at start of rule says to flatten it
# ? at start of rule says to expand it if has one child


grammar1 = r"""
start: cpt whitespace node whitespace node whitespace value;
cpt: cpt_type cpt_id;
cpt_type: 'V' | 'R';
cpt_id: integer; 
integer: '\d+';
node: integer;
value: integer;
whitespace: '\s+';
"""

grammar2 = r"""
start: cpt whitespace node whitespace node whitespace value;
cpt: cpt_type cpt_id;
cpt_type: 'V' | 'R';
cpt_id: integer; 
integer: '\d+';
node: integer;
value: integer;
whitespace: '\s+';
name: '\w+';
"""


grammar3 = """
start: cpt whitespace node whitespace node whitespace value;
cpt: cpt_type cpt_id;
cpt_type: 'V' | 'R';
cpt_id: integer; 
integer: '\d+';
node: integer;
value: integer;
whitespace: '\s+';
name: '\w+';
"""

list_parser = Grammar(grammar2)

r = list_parser.parse('V1 2 3 4')
print(r)

