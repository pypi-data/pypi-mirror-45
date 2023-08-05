from plyplus import Grammar

# @ at start of rule says to expand it
# # at start of rule says to flatten it
# ? at start of rule says to expand it if has one child

list_parser = Grammar(r"""
start: v | r;
v : vstring string sep string sep string sep value;
r : rstring string sep string sep string sep value;
vstring: '^V';
rstring: '^R';
@integer: '\d+';
@float: '-?([1-9]\d*|\d)\.(\d+)?([eE][+-]?\d+)?' | '-?([1-9]\d*|\d)[eE]([+-]?\d+)?';
string : '".*?(?<!\\)(\\\\)*?"' ;
value: float | integer | expr;
expr: '\{.*\}';
sep: '[ \t\(\),]+';
""", debug=True)

r = list_parser.parse('V1 2 3 4')
print(r)

