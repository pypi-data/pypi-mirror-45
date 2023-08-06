import ply.lex as lex
import re

text = r'V1'
token1 = r'V\s?[0-9]+'
tokens = ('TEST', )
t_TEST = token1

lexer = lex.lex(reflags=re.UNICODE, debug=1)
lexer.input(text)
for tok in lexer:
    print tok.type, tok.value, tok.lineno, tok.lexpos
