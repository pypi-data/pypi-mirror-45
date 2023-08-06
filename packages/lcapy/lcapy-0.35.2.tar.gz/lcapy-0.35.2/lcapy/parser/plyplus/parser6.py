from plyplus import Grammar

# @ at start of rule says to expand it
# # at start of rule says to flatten it
# ? at start of rule says to expand it if has one child

        #@cpt: cpt_type name;

list_parser = Grammar(r"""
start: cpt whitespace node whitespace node whitespace value;
cpt: cpt_type cpt_id;
cpt_type: 'V' | 'R';
cpt_id: integer; 
integer: '\d+';
node: integer;
value: number;
number: '\d+';
whitespace: '\s+';
""")

r = list_parser.parse('V1 2 3 4')
print(r)

