from plyplus import Grammar

# @ at start of rule says to expand it
# # at start of rule says to flatten it
# ? at start of rule says to expand it if has one child

parser = Grammar(r"""
start: v | r;
v : 'V' id? sep xnode sep xnode sep value;
r : 'R' id? sep xnode sep xnode sep value;
@id: integer | name;
@integer: '\d+';
xnode: id;
@float: '-?([1-9]\d*|\d)\.(\d+)?([eE][+-]?\d+)?' | '-?([1-9]\d*|\d)[eE]([+-]?\d+)?';
value: float | integer | expr;
expr: '\{.*\}';
// Cannot allow capital letter at start otherwise match V1 etc.
name: '[a-z]+\w*';
//word: '[a-z]+\w*';
@sep: '[ \t\(\),]+';
""", debug=True)

r = parser.parse('V1 2 3 4')
print(r)

r = parser.parse('Vfred 2 3 4')
print(r)

r = parser.parse('V 2 3 4')
print(r)

