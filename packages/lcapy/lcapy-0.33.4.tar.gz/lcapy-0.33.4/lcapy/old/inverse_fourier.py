"""This module provides support for inverse Fourier transforms.  It acts as a
wrapper for SymPy's inverse Fourier transform.  It calculates the bilateral
inverse Fourier transform using:

   s(t) = \int_{-\infty}^{\infty} S(f) e^{j * 2* \pi * t} df

It also allows functions that strictly do not have a inverse Fourier transform
by using Dirac deltas.  For example, a, cos(a * t), sin(a * t), exp(j
* a * t).


Copyright 2016 Michael Hayes, UCECE

"""

import sympy as sym

def inverse_fourier_sympy(expr, f, t):

    result = sym.inverse_fourier_transform(expr, f, t)
    if expr != 0 and result == 0:
        # There is a bug in SymPy where it returns 0.
        raise ValueError('Could not compute inverse Fourier transform for ' + str(expr))

    return result


def inverse_fourier_term(expr, f, t):

    var = sym.Symbol(str(f))
    expr = expr.replace(var, f)

    if expr.has(sym.function.AppliedUndef) and expr.args[0] == f:
        if not isinstance(expr, sym.function.AppliedUndef):
            raise ValueError('Could not compute inverse Fourier transform for ' + str(expr))

        # Convert V(f) to v(t), etc.
        name = expr.func.__name__
        name = name[0].lower() + name[1:] + '(t)'
        return sym.sympify(name)

    # Check for constant.
    if not expr.has(f):
        return expr * sym.DiracDelta(t)

    one = sym.sympify(1)
    const = one
    other = one
    exps = one
    factors = expr.as_ordered_factors()    
    for factor in factors:
        if not factor.has(f):
            const *= factor
        else:
            if factor.is_Function and factor.func == sym.exp:
                exps *= factor
            else:
                other *= factor

    if other != 1:
        if other == f:
            return const * sym.I * 2 * sym.pi * sym.DiracDelta(t, 1)
        if other == f**2:
            return const * (sym.I * 2 * sym.pi)**2 * sym.DiracDelta(t, 2)

        return inverse_fourier_sympy(expr, f, t)

    args = exps.args[0]
    foo = args / f
    if foo.has(t):
        # Have exp(a * t**n), SymPy might be able to handle this
        return inverse_fourier_sympy(expr, f, t)

    if exps != 1:
        return const * sym.DiracDelta(f - foo / (-sym.I * 2 * sym.pi))
        
    return inverse_fourier_sympy(expr, f, t)


def inverse_fourier_transform(expr, f, t):
    """Compute bilateral inverse Fourier transform of expr.

    Undefined functions such as v(t) are converted to V(f)

    This also handles some expressions that do not really have a inverse Fourier
    transform, such as a, cos(a*t), sin(a*t), exp(I * a * t).

    """

    # The variable may have been created with different attributes,
    # say when using sym.sympify('DiracDelta(f)') since this will
    # default to assuming that f is complex.  So if the symbol has the
    # same representation, convert to the desired one.

    var = sym.Symbol(str(f))
    expr = expr.replace(var, f)

    orig_expr = expr

    if expr.has(sym.cos) or expr.has(sym.sin):
        expr = expr.rewrite(sym.exp)

    terms = expr.expand().as_ordered_terms()
    result = 0

    try:
        for term in terms:
            result += inverse_fourier_term(term, f, t)
    except ValueError:
        raise ValueError('Could not compute inverse Fourier transform for ' + str(orig_expr))

    return result


def test():

     t, f, a = sym.symbols('t f a', real=True)

     print(inverse_fourier_transform(1 / (1 + sym.I * f), f, t))



