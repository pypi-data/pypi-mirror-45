from plyplus import Grammar

# @ at start of rule says to expand it
# # at start of rule says to flatten it
# ? at start of rule says to expand it if has one child

# Can't use name node if wish to display tree with dot

parser = Grammar(r"""
start: c | d | e | f | g | h | i | l | q | r | sw | v;
c: cname pnode nnode value;
cname: 'C(\d|\w)+';
d: dname pnode nnode dtype value;
dname: 'D(\d|\w)+';
dtype: 'led' | 'zener' | 'photo' | 'tunnel' | 'shottky';
e: ename pnode nnode cpnode cnnode value;
ename: 'E(\d|\w)+';
f: fname pnode nnode vname value;
fname: 'F(\d|\w)+';
g: gname pnode nnode cpnode cnnode value;
gname: 'G(\d|\w)+';
h: hname pnode nnode vname value;
hname: 'H(\d|\w)+';
i: iname pnode nnode vitype value;
iname: 'I(\d|\w)+';
l: lname pnode nnode value;
lname: 'L(\d|\w)+';
// C B E or D G S
q: qname cnode bnode enode qtype;
qname: 'Q(\d|\w)+';
qtype: 'pnp' | 'npn';
r: rname pnode nnode value;
rname: 'R(\d|\w)+';
sw: swname pnode nnode swtype;
swname: 'SW(\d|\w)+';
swtype: 'nc' | 'no' | 'push';
v: vname pnode nnode vitype value;
vname: 'V(\d|\w)+';
vitype: 'ac' | 'dc' | 'step' | 'acstep' | 'impulse' | 's';
@integer: '\d+';
value: float | integer | nul;
float: '-?([1-9]\d*|\d)\.(\d+)?([eE][+-]?\d+)?';
// Positive node
pnode: xnode;
// Negative node
nnode: xnode;
// Positive controlling node
cpnode: xnode;
// Negative controlling node
cnnode: xnode;
// Collector (drain) node
cnode: xnode;
// Base (gate) node
bnode: xnode;
// Emitter (source) node
enode: xnode;
@xnode: '\d+';
@nul: ;
WHITESPACE: '[ \t]+' (%ignore);
""")

r = parser.parse('R1 2 3 4')
print(r)

r.to_png_with_pydot('foo.png')

r1 = parser.parse('R1 2 3')
print(r1)

ra1 = parser.parse('Ra1 2 3')
print(ra1)

q1 = parser.parse('Q1 2 3 4 pnp')
print(q1)

sw1 = parser.parse('SW1 2 3 push')
print(sw1)

d1 = parser.parse('D1 2 3 led')
print(d1)
