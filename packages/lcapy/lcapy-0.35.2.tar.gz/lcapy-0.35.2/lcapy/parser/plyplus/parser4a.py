from plyplus import Grammar

# @ at start of rule says to expand it
# # at start of rule says to flatten it
# ? at start of rule says to expand it if has one child

        #@cpt: cpt_type name;

list_parser = Grammar(r"""
start: cpt whitespace node whitespace node whitespace value;
cpt: cpt_type cpt_id;
cpt_type: 'V' | 'R';
cpt_id: '[a-z]+' | integer; 
integer: '\d+';
node: integer;
value: number;
number: '\d+';
whitespace: '\s+';
""")

r = list_parser.parse('V1 2 3 4')
print(r)

r2 = list_parser.parse('Vabc 2 3 4')
print(r2)

x = r"""
start: cpt whitespace node whitespace node whitespace value;
cpt: cpt_type cpt_id;
cpt_type: 'V' | 'R';
cpt_id: '[a-z]+' | integer; 
integer: '\d+';
node: integer;
value: number;
number: '\d+';
whitespace: '\s+';
"""
