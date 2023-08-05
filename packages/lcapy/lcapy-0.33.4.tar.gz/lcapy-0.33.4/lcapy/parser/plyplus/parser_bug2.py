from plyplus import Grammar


grammar1 = r"""
start: cpt sep node;
cpt: cpt_type cpt_id;
cpt_type: 'V' | 'R';
cpt_id: integer; 
integer: '\d+';
// The following fails but '\d+' works
node: '[0-9]+';
//node: '\d+';
@sep: '\s+';
"""

parser = Grammar(grammar1, debug=True)

r = parser.parse('V1 1')
print(r)

