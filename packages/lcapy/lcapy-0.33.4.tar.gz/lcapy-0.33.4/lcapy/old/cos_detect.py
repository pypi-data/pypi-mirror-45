from lcapy import sympify, t
import sympy as sym
from sympy import symbols, I, exp, cos, pi, sin

def is_dc(val):
    """Return True if time domain expression is dc"""

    expr = getattr(val, 'expr', sympify(val))

    for symbol in expr.free_symbols:
        if symbol.name in ('s', 't', 'f', 'omega'):
            return False

    terms = expr.as_ordered_terms()
    for term in terms:
        n, d = term.as_numer_denom()
        if not ((n.is_Symbol or n.is_number) and (d.is_Symbol or d.is_number)):
            return False
    return True


class AC(object):

    def __init__(self, amp, freq, phase, var):
        self.amp = amp
        self.freq = freq
        self.phase = phase
        self.var = var

def fred(expr, var):

    if expr.func == cos:
        phase = 0
    elif expr.func == sin:
        phase = pi / 2
    else:
        raise ValueError('%s not sin/cos' % expr)

    terms = expr.args[0].as_ordered_terms()
    freq = 0
    for term in terms:
        if is_dc(term):
            phase += term
        elif var not in term.free_symbols:
            return None
        else:
            term /= var
            if var in term.free_symbols:
                return None
            freq = term / (2 * pi)

    return freq, phase


def bar(expr, var):

    factors = expr.as_ordered_factors()
    amp = 1
    freq = 0
    phase = 0
    for factor in factors:
        if factor.is_Function:
            if factor.func not in (cos, sin):
                return None
            ret = fred(factor, var)
            if ret is None:
                return None
            freq, phase = ret
        elif is_dc(factor):
            amp *= factor
        else:
            return None
    return AC(amp, freq, phase, var)


def fourier(expr, var):

    # Convert sum of exp into sin/cos
    expr = expr.rewrite(cos).combsimp().expand()

    terms = expr.as_ordered_terms()
    for term in terms:
        bar(term, var)


def foo(expr, var=t):

    # Convert sum of exp into sin/cos
    expr = expr.rewrite(cos).combsimp().expand()
    return bar(expr, var)


j = I
x = symbols('x', real=True)

y1 = 5 * exp(j * 2 * pi * x * 2) + 5 * exp(-j * 2 * pi * x * 2)
y2 = 3 * exp(j * 2 * pi * x * 4) + 3 * exp(-j * 2 * pi * x * 4)
y3 = -j * 4 * exp(j * 2 * pi * x * 4) + j * 4 * exp(-j * 2 * pi * x * 4)

y4 = 10 * sin(2 * pi * 5 * x + pi / 4)

y = y1 + y2 + y3

z = y.rewrite(cos)

a4 = foo(y4, x)
