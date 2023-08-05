# Could have separate line for each component subtype
grammar = r"""start: c | d | e | f | g | h | i | l | q | qpnp | qnpn | r | sw | v;
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
qpnp: qname cnode bnode enode 'pnp';
qnpn: qname cnode bnode enode 'npn';
q: qname cnode bnode enode;
qname: 'Q(\d|\w)+';
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
"""
