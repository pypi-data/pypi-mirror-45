from plyplus import Grammar

# @ at start of rule says to expand it
# # at start of rule says to flatten it
# ? at start of rule says to expand it if has one child

        #@cpt: cpt_type name;

list_parser = Grammar(r"""
start: v | r;
v : 'V' cptid xnode xnode value;
r : 'R' cptid xnode xnode value;
cptid: '\d+';
@xnode: '\d+';
@integer: '\d+';
@float: '-?([1-9]\d*|\d)\.(\d+)?([eE][+-]?\d+)?' | '-?([1-9]\d*|\d)[eE]([+-]?\d+)?';
value: float | integer | '\{.*\}';
//WHITESPACE: '[ \t\(\),]+' (%ignore);
""")

r = list_parser.parse('V1 2 3 4')
print(r)

