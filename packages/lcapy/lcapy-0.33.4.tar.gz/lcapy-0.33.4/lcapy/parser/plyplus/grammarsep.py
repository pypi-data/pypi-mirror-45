grammar = r"""
start: c | d | e | f | g | h | i | k | l | q | r | sw | v;
c: cname sep pnode sep nnode optvalue;
cname: 'C(\d|\w)+';
d: dname sep pnode sep nnode sep dtype optvalue;
dname: 'D(\d|\w)+';
dtype: 'led' | 'zener' | 'photo' | 'tunnel' | 'shottky';
e: ename sep pnode sep nnode sep cpnode sep cnnode optvalue;
ename: 'E(\d|\w)+';
f: fname sep pnode sep nnode sep vname optvalue;
fname: 'F(\d|\w)+';
g: gname sep pnode sep nnode sep cpnode sep cnnode optvalue;
gname: 'G(\d|\w)+';
h: hname sep pnode sep nnode sep vname optvalue;
hname: 'H(\d|\w)+';
i: iname sep pnode sep nnode sep vitype optvalue;
iname: 'I(\d|\w)+';
k: kname lname lname optvalue;
kname: 'K(\d|\w)+';
l: lname sep pnode sep nnode optvalue;
lname: 'L(\d|\w)+';
// C B E or D G S
q: qname cnode sep bnode sep enode sep qtype;
qname: 'Q(\d|\w)+';
qtype: 'pnp' | 'npn' | nul;
r: rname sep pnode sep nnode optvalue;
rname: 'R(\d|\w)+';
sw: swname sep pnode sep nnode sep swtype;
swname: 'SW(\d|\w)+';
swtype: 'nc' | 'no' | 'push';
v: vname sep pnode sep nnode sep vitype optvalue;
vname: 'V(\d|\w)+';
vitype: 'ac' | 'dc' | 'step' | 'acstep' | 'impulse' | 's' | nul;
@integer: '\d+';
value: float | integer | nul;
optvalue: (sep value) | nul;
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
@xnode: '\w+';
@nul: ;
sep: '[ \t,]+');
"""

