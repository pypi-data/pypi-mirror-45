from plyplus import Grammar

# @ at start of rule says to expand it
# # at start of rule says to flatten it
# ? at start of rule says to expand it if has one child

        #@cpt: cpt_type name;

# Can't use name node if wish to display tree with dot

list_parser = Grammar(r"""
start: rlcvi;
rlcvi: cpt nnode nnode value;
cpt: cpt_type cpt_id;
cpt_type: 'V' | 'R';
integer: '\d+';
value: float | integer;
float: '-?([1-9]\d*|\d)\.(\d+)?([eE][+-]?\d+)?';
cpt_id: '\d+'; 
nnode: integer;
WHITESPACE: '[ \t]+' (%ignore);
""")

r = list_parser.parse('V1 2 3 4')
print(r)

r.to_png_with_pydot('foo.png')

#cpt_id: '\w+'; 
