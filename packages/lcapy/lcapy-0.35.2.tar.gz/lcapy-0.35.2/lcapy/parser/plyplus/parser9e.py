from plyplus import Grammar

# @ at start of rule says to expand it
# # at start of rule says to flatten it
# ? at start of rule says to expand it if has one child

# Can't use name node if wish to display tree with dot

list_parser = Grammar(r"""
start: c | d | e | f | g | h | i | l | q | r | sw | v;
c: 'C' cpt_id sep pnode sep nnode opt_value;
d: 'D' cpt_id sep pnode sep nnode sep d_type opt_value;
d_type: 'led' | 'zener' | 'photo' | 'tunnel' | 'shottky';
e: 'E' cpt_id sep pnode sep nnode sep sep cpnode sep cnnode opt_value;
f: 'F' cpt_id sep pnode sep nnode sep 'V' cpt_id opt_value;
g: 'G' cpt_id sep pnode sep nnode sep sep cpnode sep cnnode opt_value;
h: 'H' cpt_id sep pnode sep nnode sep 'V' cpt_id opt_value;
i: 'I' cpt_id sep pnode sep nnode sep vi_type opt_value;
l: 'L' cpt_id sep pnode sep nnode opt_value;
q: 'Q'cpt_id sep pnode sep nnode sep nnode sep q_type;
q_type: 'pnp' | 'npn';
r: rname sep pnode sep nnode opt_value;
rname: 'R(\d|\w)+';
sw: 'SW' cpt_id sep pnode sep nnode sep sw_type;
sw_type: 'nc' | 'no' | 'push';
v: 'V' cpt_id sep pnode sep nnode vi_type opt_value;
vi_type: 'ac' | 'dc' | 'step' | 'acstep' | 'impulse' | 's';
integer: '\d+';
value: float | integer | nul;
opt_value: (sep value) | nul;
float: '-?([1-9]\d*|\d)\.(\d+)?([eE][+-]?\d+)?';
//cpt_id: '\d+' | '[a-z]+'; 
//cpt_id: '[0-9]+'; 
cpt_id: '\d+'; 
pnode: xnode;
nnode: xnode;
cpnode: xnode;
cnnode: xnode;
xnode: '\d+';
nul: ;
@sep: '[ \t,]+';
""")




r = list_parser.parse('R1 2 3 4')
print(r)


rc = list_parser.parse('R1,2,3,4')
print(rc)

r.to_png_with_pydot('foo.png')

r1 = list_parser.parse('R1 2 3')
print(r1)

ra1 = list_parser.parse('Ra1 2 3')
print(ra1)

q = list_parser.parse('Q1 2 3 4 pnp')
print(q)

s = list_parser.parse('SW1 2 3 push')
print(s)

d = list_parser.parse('D1 2 3 led')
print(d)


#cpt_id: '\w+'; 
