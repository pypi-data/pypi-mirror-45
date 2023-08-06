from plyplus import Grammar

# @ at start of rule says to expand it
# # at start of rule says to flatten it
# ? at start of rule says to expand it if has one child

        #@cpt: cpt_type name;

# Can't use name node if wish to display tree with dot

list_parser = Grammar(r"""
start: rlc | q | vi | switch;
rlc: ('R' | 'L' | 'C') cpt_id nnode nnode value;
vi: ('V' | 'I') cpt_id nnode nnode vi_type value;
vi_type: 'ac' | 'dc' | 'step' | 'acstep' | 'impulse' | 's'
q: 'Q' cpt_id nnode nnode nnode q_type;
q_type: 'pnp' | 'npn';
switch: 'SW' cpt_id nnode nnode switch_type;
switch_type: 'nc' | 'no' | 'push';
integer: '\d+';
value: float | integer | nul;
float: '-?([1-9]\d*|\d)\.(\d+)?([eE][+-]?\d+)?';
cpt_id: '\d+'; 
nnode: integer;
nul: ;
WHITESPACE: '[ \t]+' (%ignore);
""")




r = list_parser.parse('R1 2 3 4')
print(r)

r.to_png_with_pydot('foo.png')

r1 = list_parser.parse('R1 2 3')
print(r1)

q = list_parser.parse('Q1 2 3 4 pnp')
print(q)

s = list_parser.parse('SW1 2 3 push')
print(s)


#cpt_id: '\w+'; 
