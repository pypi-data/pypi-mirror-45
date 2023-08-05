from plyplus import Grammar

# @ at start of rule says to expand it
# # at start of rule says to flatten it
# ? at start of rule says to expand it if has one child

parser = Grammar(r"""
start: v | r;
v : 'V' name xnode xnode value;
r : 'R' name xnode xnode value;
@name: integer | id;
@integer: '\d+';
xnode: name;
@float: '-?([1-9]\d*|\d)\.(\d+)?([eE][+-]?\d+)?' | '-?([1-9]\d*|\d)[eE]([+-]?\d+)?';
value: float | integer | expr;
expr: '\{.*\}';
// Cannot allow capital letter at start otherwise match V1 etc.
id: '[a-z]+\w*';
//word: '[a-z]+\w*';
WHITESPACE: '[ \t\(\),]+' (%ignore);
""", debug=True)

r = parser.parse('V1 2 3 4')
print(r)

r = parser.parse('V fred 2 3 4')
print(r)

