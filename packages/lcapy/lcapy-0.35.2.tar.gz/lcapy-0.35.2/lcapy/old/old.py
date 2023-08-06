    @property
    def xvals_flip(self):
        return self.xmin + self.xmax - self.xvals

    @property
    def yvals_flip(self):
        return self.ymin + self.ymax - self.yvals

    @property
    def xmin(self):
        return self.xvals.min()

    @property
    def xmax(self):
        return self.xvals.max()

    @property
    def ymin(self):
        return self.yvals.min()

    @property
    def ymax(self):
        return self.yvals.max()

    @property
    def xextent(self):
        return self.xmax - self.xmin

    @property
    def yextent(self):
        return self.ymax - self.ymin



    @property
    def Vd(self):
        """Return dictionary of s-domain branch voltage differences
        indexed by component name"""

        if hasattr(self, '_Vd'):
            return self._Vd

        self._solve()

        # This is a hack.  The assumptions should be recalculated
        # when performing operations on Expr types.
        assumptions = self.assumptions

        self._Vd = {}
        for elt in self.elements.values():
            if elt.type == 'K':
                continue
            n1, n2 = self.node_map[elt.nodes[0]], self.node_map[elt.nodes[1]]
            self._Vd[elt.name] = Vtype((self._V[n1] - self._V[n2]).simplify(),
                                       **assumptions)

        return self._Vd


    @property
    def v(self):
        """Return dictionary of t-domain node voltages indexed by node name
        and voltage differences indexed by branch name."""

        if not hasattr(self, '_vcache'):
            self._vcache = Ldict(self.V, **self.assumptions)

        return self._vcache

    @property
    def i(self):
        """Return dictionary of t-domain branch currents indexed
        by component name."""

        if not hasattr(self, '_icache'):
            self._icache = Ldict(self.I, **self.assumptions)

        return self._icache


class Mdict(dict):

    def __init__(self, branchdict, **assumptions):

        super(Mdict, self).__init__()
        self.branchdict = branchdict
        # Hack, should compute assumptions on fly.
        self.assumptions = assumptions

    def __getitem__(self, key):

        # If key is an integer, convert to a string.
        if isinstance(key, int):
            key = '%d' % key

        if key in self.branchdict:
            n1, n2 = self.branchdict[key]
            return Vtype((self[n1] - self[n2]).simplify(), **self.assumptions)

        return super(Mdict, self).__getitem__(key)

    def keys(self):

        return list(super(Mdict, self).keys()) + list(self.branchdict)


    
    def __getitem__(self, key):

        # If key is an integer, convert to a string.
        if isinstance(key, int):
            key = '%d' % key

        return self.nodes[key]
    


class Thevenin(OnePort):
    """Thevenin (Z) model
    ::

             +------+    +-------------------+
        I1   | +  - |    |                   | -I1
        -->--+  V   +----+        Z          +--<--
             |      |    |                   |
             +------+    +-------------------+
        +                       V1                -
    """

    def __init__(self, Zval=Zs(0), Vval=Vs(0)):

        # print('<T> Z:', Zval, 'V:', Vval)
        if not isinstance(Zval, Zs):
            raise ValueError('Zval not Zs')
        if not isinstance(Vval, Vs):
            raise ValueError('Vval not Vs')
        self.Z = Zval
        self.Voc = Vval

        super(Thevenin, self).__init__()

    @property
    def Y(self):
        return Ys(1 / self.Z)

    @property
    def Isc(self):

        assumptions = self.Voc.assumptions
        return Itype(self.Voc / self.Z, **assumptions)

    def parallel_ladder(self, *args):
        """Add unbalanced ladder network in parallel;
        alternately in parallel and series.

        ::

               +---------+       +---------+
            +--+   self  +---+---+   Z1    +---+---
            |  +---------+   |   +---------+   |
            |              +-+-+             +-+-+
            |              |   |             |   |
            |              |Z0 |             |Z2 |
            |              |   |             |   |
            |              +-+-+             +-+-+
            |                |                 |
            +----------------+-----------------+---
        """

        ret = self
        for m, arg in enumerate(args):
            if m & 1:
                ret = ret.series(arg)
            else:
                ret = ret.parallel(arg)
        return ret

    def parallel_C(self, Z0, Z1, Z2):
        """Add C network in parallel.

        ::

               +---------+      +---------+
            +--+   self  +------+   Z0    +---+----
            |  +---------+      +---------+   |
            |                               +-+-+
            |                               |   |
            |                               |Z1 |
            |                               |   |
            |                               +-+-+
            |                   +---------+   |
            +-------------------+   Z2    +---+----
                                +---------+
        """

        return self.series(Z0).series(Z2).parallel(Z1)

    def parallel_L(self, Z0, Z1):
        """Add L network in parallel.

        ::

               +---------+      +---------+
            +--+   self  +------+   Z0    +---+----
            |  +---------+      +---------+   |
            |                               +-+-+
            |                               |   |
            |                               |Z1 |
            |                               |   |
            |                               +-+-+
            |                                 |
            +---------------------------------+----
        """

        return self.series(Z0).parallel(Z1)

    def parallel_pi(self, Z0, Z1, Z2):
        """Add Pi (Delta) network in parallel.

        ::

               +---------+       +---------+
            +--+   self  +---+---+   Z1    +---+---
            |  +---------+   |   +---------+   |
            |              +-+-+             +-+-+
            |              |   |             |   |
            |              |Z0 |             |Z2 |
            |              |   |             |   |
            |              +-+-+             +-+-+
            |                |                 |
            +----------------+-----------------+---
        """

        return (self.parallel(Z0) + Z1).parallel(Z2)

    def parallel_T(self, Z0, Z1, Z2):
        """Add T (Y) network in parallel.
        ::

               +---------+       +---------+        +---------+
            +--+   self  +-------+   Z0    +---+----+   Z2    +---
            |  +---------+       +---------+   |    +---------+
            |                                +-+-+
            |                                |   |
            |                                |Z1 |
            |                                |   |
            |                                +-+-+
            |                                  |
            +----------------------------------+------------------
        """

        return (self.parallel(Z0) + Z1).parallel(Z2)

    def cpt(self):
        """Convert to a component, if possible"""

        if self.Z.is_number and self.Voc == 0:
            return R(self.Z.expr)

        v = s * self.Voc
        if self.Z == 0 and v.is_number:
            return Vdc(v.expr)

        i = s * self.Isc
        if self.Y == 0 and i.is_number:
            return Idc(i.expr)

        y = s * self.Y
        z = s * self.Z

        if z.is_number and v.is_number:
            return C((1 / z).expr, v)

        if y.is_number and i.is_number:
            return L((1 / y).expr, i)

        if self.Voc == 0:
            return Z(self.Z.expr)

        return self

    def smodel(self):
        """Convert to s-domain"""

        if self.Voc == 0:
            return Z(self.Z)
        if self.Z == 0:
            return sV(self.Voc)
        return Ser(sV(self.Voc), Z(self.Z))


class Norton(OnePort):
    """Norton (Y) model
    ::

                +-------------------+
        I1      |                   |      -I1
        -->-+---+        Y          +---+--<--
            |   |                   |   |
            |   +-------------------+   |
            |                           |
            |                           |
            |          +------+         |
            |          |      |         |
            +----------+ -I-> +---------+
                       |      |
                       +------+

          +              V1                 -
    """

    def __init__(self, Yval=Ys(0), Ival=Is(0)):

        # print('<N> Y:', Yval, 'I:', Ival)
        if not isinstance(Yval, Ys):
            raise ValueError('Yval not Ys')
        if not isinstance(Ival, Is):
            raise ValueError('Ival not Is')
        self.Y = Yval
        self.Isc = Ival

        super(Norton, self).__init__()

    @property
    def Z(self):
        return Zs(1 / self.Y)

    @property
    def Voc(self):
        return Vtype(self.Isc / self.Y, **self.Isc.assumptions)

    def cpt(self):
        """Convert to a component, if possible"""

        if self.Y.is_number and self.Isc == 0:
            return G(self.Y.expr)

        i = s * self.Isc
        if self.Y == 0 and i.is_number:
            return Idc(i.expr)

        v = s * self.Voc
        if self.Z == 0 and v.is_number:
            return Vdc(v.expr)

        y = s * self.Y
        z = s * self.Z

        if z.is_number and v.is_number:
            return C((1 / z).expr, v)

        if y.is_number and i.is_number:
            return L((1 / y).expr, i)

        if self.Isc == 0:
            return Y(self.Y.expr)

        return self

    def smodel(self):
        """Convert to s-domain"""

        if self.Isc == 0:
            return Y(self.Y)
        if self.Y == 0:
            return sI(self.Isc)
        return Par(sI(self.Isc), Y(self.Y))


The components are represented by either Thevenin or Norton one-port
networks with the following attributes:

Zoc open-circuit impedance
Ysc short-circuit admittance
Voc open-circuit voltage
Isc short-circuit current



    def select(self, kind):
        result = 0
        for val in self:
            if type(val) == self.type_map[kind]:
                if kind == 'n':
                    val = val * val
                result += val
        if kind == 'n':
            result = sqrt(result)
        return result


class tsExpr(sExpr):

    """t or s-domain expression or symbol, interpreted in time domain
    if not containing s"""

    # Todo, replace with a factory.

    def __init__(self, val, **assumptions):

        assumptions = {}

        # If no s in expression evaluate as tExpr and convert to s-domain.
        if 's' not in symbols_find(val):
            tval = tExpr(val)
            val = tval.laplace().expr
            val = val.subs(context.symbols)
            assumptions = tval.assumptions

        super(tsExpr, self).__init__(val, real=True, **assumptions)


    
    def __add__(self, x):
        if isinstance(x, noiseExpr):
            # Assume uncorrelated
            val = Expr(self)
            x = Expr(x)
            return self.__class__(sqrt(val * val + x * x))
        return super(noiseExpr, self).__add__(x)

    def __sub__(self, x):
        # Cannot tell if correlated/
        raise ValueError('Cannot subtract noise spectra')

    def __mul__(self, x):
        # Cannot tell if correlated/
        raise ValueError('Cannot multiply noise spectra')

    def __div__(self, x):
        # Cannot tell if correlated/
        raise ValueError('Cannot divide noise spectra')            
        
    
    # Hack for debugging.  Otherwise sym.sympify will convert Expr
    # types to string and then re-parse.  Unfortunately, we change I
    # to j when printing and so j gets converted into a symbol and not
    # the imaginary unit.
    if hasattr(expr, 'expr'):
        expr = expr.expr
    if hasattr(t, 'expr'):
        t = t.expr
    if hasattr(f, 'expr'):
        f = f.expr

    expr = sym.sympify(expr)
    t = sym.sympify(t)
    f = sym.sympify(f)


    @property
    def assumptions(self):

        assumptions = {}
        for attr in all_assumptions:
            assumption = getattr(self, 'is_' + attr)
            if assumption is not None:
                assumptions[attr] = assumption
        return assumptions

    @assumptions.setter
    def assumptions(self, **assumptions):

        for attr in all_assumptions:
            if attr in assumptions:
                setattr(self, 'is_' + attr, assumptions.pop(attr))
        if assumptions != {}:
            raise ValueError('Unknown assumption %s' % assumptions)

    
