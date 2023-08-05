from sympy.parsing.sympy_parser import parse_expr, auto_number
from sympy.parsing.sympy_tokenize import NUMBER, STRING, NAME, OP
from sympy import Basic, Symbol, Expr
import re

global_dict = {}
exec('from sympy import *', global_dict)
global_dict.pop('E1')
# delta gets printed as DiracDelta; could override
global_dict['delta'] = global_dict['DiracDelta']
global_dict['step'] = global_dict['Heaviside']

cpt_names = ('C', 'E', 'F', 'G', 'H', 'I', 'L', 'R', 'V', 'Y', 'Z')
cpt_name_pattern = re.compile(r"(%s)([\w']*)" % '|'.join(cpt_names))

braces_suffix_pattern = re.compile(r"^([a-zA-Z]+[\w]*_){([\w]*)}$")

def canonical_name(name):

    match = braces_suffix_pattern.match(name)
    if match:
        # Convert R_{out} to R_out for sympy to recognise.
        name = match.groups()[0] + match.groups()[1]
        return name

    if name.find('_') != -1:
        return name

    # Rewrite R1 as R_1, etc.
    match = cpt_name_pattern.match(name)
    if match:
        if match.groups()[1] == '':
            return name
        name = match.groups()[0] + '_' + match.groups()[1]
        return name

    return name


def parse(string, symbols={}, evaluate=True, local_dict={}, **assumptions):

    cache = assumptions.pop('cache', True)

    def auto_symbol(tokens, local_dict, global_dict):
        """Inserts calls to ``Symbol`` for undefined variables."""
        result = []
        prevTok = (None, None)

        tokens.append((None, None))  # so zip traverses all tokens
        for tok, nextTok in zip(tokens, tokens[1:]):
            tokNum, tokVal = tok
            nextTokNum, nextTokVal = nextTok
            if tokNum == NAME:
                name = tokVal

                if name in local_dict:
                    result.append((NAME, name))
                    continue

                elif name in global_dict:

                    obj = global_dict[name]
                    if isinstance(obj, (Basic, type)):
                        result.append((NAME, name))
                        continue

                    if callable(obj):
                        result.append((NAME, name))
                        continue

                    # This does not work, say with delta * 5.
                    # if (callable(obj) and
                    #     nextTokNum == OP and nextTokVal == '('):
                    #     result.append((NAME, name))
                    #     continue

                name = repr(canonical_name(str(name)))

                # Automatically add Symbol
                result.extend([(NAME, 'Symbol'), (OP, '('), (NAME, name)])
                for assumption, val in assumptions.iteritems():
                    result.extend([(OP, ','), 
                                   (NAME, '%s=%s' % (assumption, val))])
                result.extend([(OP, ')')])

            else:
                result.append((tokNum, tokVal))

            prevTok = (tokNum, tokVal)

        return result

    s = parse_expr(string, transformations=(auto_symbol, auto_number), 
                   global_dict=global_dict, local_dict=local_dict,
                   evaluate=evaluate)
    
    # Look for newly defined symbols.
    for symbol in s.atoms(Symbol):
        if symbol.name in symbols and symbols[symbol.name] != symbol:
            # The symbol may have different assumptions, real,
            # positive, etc.
            print('Different assumptions for symbol %s' % symbol.name)

        if cache and symbol.name not in symbols:
            symbols[symbol.name] = symbol

    return s


def sympify(arg, symbols={}, evaluate=True, **assumptions):
    """Create a sympy expression."""

    if isinstance(arg, (Symbol, Expr)):
        return arg

    # Why doesn't sympy do this?
    if isinstance(arg, complex):
        re = sym.sympify(str(arg.real), rational=True, evaluate=evaluate)
        im = sym.sympify(str(arg.imag), rational=True, evaluate=evaluate)
        if im == 1.0:
            arg = re + sym.I
        else:
            arg = re + sym.I * im
        return arg

    if isinstance(arg, float):
        # Note, need to convert to string to achieve a rational
        # representation.
        return sym.sympify(str(arg), rational=True, evaluate=evaluate)
        
    if isinstance(arg, str):
        return parse(arg, symbols, evaluate=evaluate, local_dict=symbols, 
                     **assumptions)

    return sym.sympify(arg, rational=True, locals=symbols, 
                       evaluate=evaluate)


def symbol(name, symbols={}, **assumptions):

    return sympify(name, symbols, evaluate=True, **assumptions)


symbols = {}
s1 = sympify('5 * E1 + a', symbols)
s2 = sympify('5 * R1 + a', symbols, real=True)
print(symbols['R_1'].assumptions0)
s3 = sympify('5 * R1 + a', symbols, positive=True)
print(symbols['R_1'].assumptions0)

