from lcapy import sympify, t
import sympy as sym
from sympy import symbols, I, exp, cos, pi, sin

class Causal(object):

    def _has_causal_factor(self, expr):

        factors = expr.as_ordered_factors()
        for factor in factors:
            if factor == 0:
                return True
            if (not factor.is_Function 
                or factor.func not in (sym.Heaviside, sym.DiracDelta)):
                continue

            p = sym.Poly(factor.args[0], self.var)
            coeffs = p.all_coeffs()
            if len(coeffs) != 2:
                return False
            print(coeffs)

            if (coeffs[0].is_positive 
                and (coeffs[1].is_positive or coeffs[1].is_zero)):
                return True

        return False        

    def _is_causal(self, expr):

        terms = expr.as_ordered_terms()
        for term in terms:
            if not self._has_causal_factor(term):
                return False
                
        return True

    def __init__(self, expr, var=t):        

        self.var = getattr(var, 'expr', sympify(var))
        self.causal = self._is_causal(getattr(expr, 'expr', sympify(expr)))


class DC(object):

    def _is_dc(self, expr):

        if self.var in expr.free_symbols:
            return False

        terms = expr.as_ordered_terms()
        for term in terms:
            for factor in term.as_ordered_factors():
                n, d = factor.as_numer_denom()
                if not ((n.is_Symbol or n.is_number) and (d.is_Symbol or d.is_number)):
                    return False
        return True

    def __init__(self, expr, var=t):        

        self.var = getattr(var, 'expr', sympify(var))
        self.dc = self._is_dc(getattr(expr, 'expr', sympify(expr)))


class AC(object):

    def _find_freq_phase(self, expr):

        self.freq = 0

        if expr.func == cos:
            self.phase = 0
        elif expr.func == sin:
            self.phase = pi / 2
        else:
            raise ValueError('%s not sin/cos' % expr)
            
        p = sym.Poly(expr.args[0], self.var)
        coeffs = p.all_coeffs()
        if len(coeffs) != 2:
            return False

        self.phase += coeffs[1]
        self.freq = coeffs[0] / (2 * pi)
        return True

    def _is_ac(self, expr):

        # Convert sum of exps into sin/cos
        expr = expr.rewrite(cos).combsimp().expand()
        
        factors = expr.as_ordered_factors()
            
        self.amp = 1
        for factor in factors:
            if factor.is_Function:
                if factor.func not in (cos, sin):
                    return False
                if not self._find_freq_phase(factor):
                    return False
            elif DC(factor).dc:
                self.amp *= factor
            else:
                return False
        return True

    def __init__(self, expr, var=t):

        self.var = getattr(var, 'expr', sympify(var))
        self.amp = 0
        self.freq = 0
        self.phase = 0
        self.ac = self._is_ac(getattr(expr, 'expr', sympify(expr)))



j = I
x = symbols('x', real=True)

y1 = 5 * exp(j * 2 * pi * x * 2) + 5 * exp(-j * 2 * pi * x * 2)
y2 = 3 * exp(j * 2 * pi * x * 4) + 3 * exp(-j * 2 * pi * x * 4)
y3 = -j * 4 * exp(j * 2 * pi * x * 4) + j * 4 * exp(-j * 2 * pi * x * 4)

y4 = 10 * sin(2 * pi * 5 * x + pi / 4)

y = y1 + y2 + y3

z = y.rewrite(cos)

a4 = AC(y4, x)
