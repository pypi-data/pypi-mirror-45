grammar = r"""
start: c | d | e | f | g | h | i | jnjf | jpjf | k | l | qnpn | qpnp | r | sw | v | vdc | vac | vsin;
c: cname pnode nnode value?;
cname: 'C(\d|\w)+';
d: dname pnode nnode dtype value?;
dname: 'D(\d|\w)+';
dtype: 'led' | 'zener' | 'photo' | 'tunnel' | 'shottky';
e: ename pnode nnode cpnode cnnode value?;
ename: 'E(\d|\w)+';
f: fname pnode nnode vname value?;
fname: 'F(\d|\w)+';
g: gname pnode nnode cpnode cnnode value?;
gname: 'G(\d|\w)+';
h: hname pnode nnode vname value?;
hname: 'H(\d|\w)+';
i: iname pnode nnode vitype value?;
iname: 'I(\d|\w)+';
jnjf: jname dnode gnode snode 'njf'?;
jpjf: jname dnode gnode snode 'pjf';
jname: 'J(\d|\w)+';
k: kname lname lname value?;
kname: 'K(\d|\w)+';
l: lname pnode nnode value?;
lname: 'L(\d|\w)+';
// C B E or D G S
qnpn: qname cnode bnode enode 'npn'?;
qpnp: qname cnode bnode enode 'pnp';
qname: 'Q(\d|\w)+';
r: 'R'name pnode nnode value?;
name: '(\d|\w)+';
sw: swname pnode nnode swtype;
swname: 'SW(\d|\w)+';
swtype: 'nc' | 'no' | 'push';
v: vname pnode nnode value?;
vdc: vname pnode nnode 'dc' value?;
vac: vname pnode nnode 'ac' value? phase?;
vsin: vname pnode nnode 'sin' vo va fo td? alpha? phase?;
vo: value;
va: value;
fo: value;
td: value;
alpha: value;
phase: value;
vname: 'V(\d|\w)+';
vitype: 'ac' | 'dc' | 'step' | 'acstep' | 'impulse' | 's' | nul;
@integer: '\d+';
value: float | integer | '\{.*\}';
float: '-?([1-9]\d*|\d)\.(\d+)?([eE][+-]?\d+)?' | '-?([1-9]\d*|\d)[eE]([+-]?\d+)?';
// Positive node
pnode: xnode;
// Negative node
nnode: xnode;
// Positive controlling node
cpnode: xnode;
// Negative controlling node
cnnode: xnode;
// Collector node
cnode: xnode;
// Base node
bnode: xnode;
// Emitter node
enode: xnode;
// Drain node
dnode: xnode;
// Gate node
gnode: xnode;
// Source node
snode: xnode;
@xnode: '\d+';
@nul: ;
// WHITESPACE: '[ \t,=\(\)]+' (%ignore);
WHITESPACE: '[ \t\(\)=,]+' (%ignore);
"""
