class Zjw(sfwExpr):
    """Phasor impedance aka complex impedance"""

    def __init__(self, val, **assumptions):

        super(Zjw, self).__init__(val, **assumptions)
        self._laplace_conjugate_class = Zt

    def cpt(self):

        if self.is_number:
            return R(self.expr)

        z = self * sym.I * omega

        if z.is_number:
            return C((1 / z).expr)

        z = self / (sym.I * omega)

        if z.is_number:
            return L(z.expr)

        return Z(self)


class Yjw(sfwExpr):
    """Phasor admittance aka complex admittance"""

    def __init__(self, val, **assumptions):

        super(Yjw, self).__init__(val, **assumptions)
        self._laplace_conjugate_class = Yt

    def cpt(self):

        if self.is_number:
            return G(self.expr)

        y = self * sym.I * omega

        if y.is_number:
            return L((1 / y).expr)

        y = self / (sym.I * omega)

        if y.is_number:
            return C(y.expr)

        return Y(self)


class Hjw(sfwExpr):
    """Phasor transfer function"""

    def __init__(self, val, **assumptions):

        super(Hjw, self).__init__(val, **assumptions)
        self._laplace_conjugate_class = Ht



def format_label(s):

    if s == '':
        return s

    # If have $ in string then assume necessary parts are in math-mode.
    if '$' in s:
        return latex_str(s)

    # If have _, ^, or \ need to be in math-mode.
    if '_' in s or '^' in s or '\\' in s:
        return '$' + latex_str(s) + '$'
    return s



    def label_braces(self, **kwargs):
        """Return label enclosed in braces."""

        label = self.label()
        if label[0] == '{' and label[-1] =='}':
            return label
        return '{' + label + '}'

