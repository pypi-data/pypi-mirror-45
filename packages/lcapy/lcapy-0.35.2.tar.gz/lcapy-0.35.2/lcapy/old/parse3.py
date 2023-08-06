from sympy.parsing.sympy_parser import parse_expr, standard_transformations
from sympy.parsing.sympy_tokenize import generate_tokens, untokenize, TokenError, NUMBER, STRING, NAME, OP, ENDMARKER
from keyword import iskeyword
from sympy import Basic

# To remove E1, create global_dict and remove E1, etc.

def my_symbol(tokens, local_dict, global_dict):
    """Inserts calls to ``Symbol`` for undefined variables."""
    result = []
    prevTok = (None, None)

    tokens.append((None, None))  # so zip traverses all tokens
    for tok, nextTok in zip(tokens, tokens[1:]):
        tokNum, tokVal = tok
        nextTokNum, nextTokVal = nextTok
        if tokNum == NAME:
            name = tokVal

            print(name)

            if (name in ['True', 'False', 'None']
                or iskeyword(name)
                or name in local_dict
                # Don't convert attribute access
                or (prevTok[0] == OP and prevTok[1] == '.')
                # Don't convert keyword arguments
                or (prevTok[0] == OP and prevTok[1] in ('(', ',')
                    and nextTokNum == OP and nextTokVal == '=')):
                result.append((NAME, name))
                continue
            elif name in global_dict and name != 'E1':

                # E1 is in the global dict...
                import pdb
                pdb.set_trace()
                print('Global', name)

                obj = global_dict[name]
                if isinstance(obj, (Basic, type)) or callable(obj):
                    result.append((NAME, name))
                    continue

            # Automatically add Symbol
            result.extend([
                (NAME, 'Symbol'),
                (OP, '('),
                (NAME, repr(str(name))),
                (OP, ')'),
            ])
        else:
            result.append((tokNum, tokVal))

        prevTok = (tokNum, tokVal)

    return result


def parse(string):

#    return parse_expr(string, transformations=(my_symbol,) + standard_transformations)
    return parse_expr(string, transformations=(my_symbol,))


s = parse('5 * E1 + a')
