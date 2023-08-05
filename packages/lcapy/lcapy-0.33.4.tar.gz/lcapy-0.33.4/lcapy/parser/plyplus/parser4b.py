from plyplus import Grammar

# @ at start of rule says to expand it
# # at start of rule says to flatten it
# ? at start of rule says to expand it if has one child

        #@cpt: cpt_type name;


import pdb
pdb.set_trace()

list_parser = Grammar(r"""
start: v | r;
v : vname cptid sep xnode sep xnode sep value;
r : rname cptid sep xnode sep xnode sep value;
vname: 'V';
rname: 'R';
//cptid: '\w+';
cptid: '[0-9]+';
@xnode: '\d+';
@integer: '\d+';
@float: '-?([1-9]\d*|\d)\.(\d+)?([eE][+-]?\d+)?' | '-?([1-9]\d*|\d)[eE]([+-]?\d+)?';
value: float | integer | '\{.*\}';
sep: '[ \t\(\),]+';
""", debug=True)

r = list_parser.parse('V1 2 3 4')
print(r)

