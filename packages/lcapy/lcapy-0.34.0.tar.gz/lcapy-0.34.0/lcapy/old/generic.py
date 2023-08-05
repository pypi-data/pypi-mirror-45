from .sym import sympify
from .expr import Expr
from .printing import pprint, pretty, print_str, latex
from .symbols import s, t, f, omega, j, pi

class Generic(Expr):

    def __init__(self, value):

        if value.has(s):
            self.var = s
        elif value.has(t):
            self.var = t
        elif value.has(f):
            self.var = f            
        elif value.has(omega):
            self.var = omega
        elif value.is_constant:
            # Default var
            self.var = s
        else:
            raise ValueError('Cannot determine underlying type for %s' % value)

        super (Generic, self).__init__(value)

    def __call__(self, arg, **assumptions):
        """
        arg determines the returned representation
          t: time-domain representation
          s: Laplace domain representation
          f: Fourier representation
          omega: Fourier representation (angular frequency)

        For example, V(t), V(f), or V(2 * t).

        If arg is a constant, the time-domain representation
        evaluated at the argument is returned, for example,
        V(0) returns the dc value.
        """

        try:
            arg.has(t)
        except:
            arg = sympify(arg)            
        
        if arg.has(t):
            return self.time(**assumptions).subs(t, arg)
        elif arg.has(s):
            return self.laplace(**assumptions).subs(s, arg)
        elif arg.has(f):
            return self.fourier(**assumptions).subs(f, arg)
        elif arg.has(omega):
            if self.has(omega):
                raise ValueError('Cannot return angular Fourier domain representation for expression %s that depends on %s' % (self, omega))
            return self.fourier(**assumptions)(arg).subs(f, omega / (2 * pi))
        elif arg.is_constant():
                return self.__class__(self.subs(self.var, arg))
        else:
            raise ValueError('Can only return t, f, s, or omega domains')

    def time(self, **assumptions):

        if self.var == t:
            return self
        
        assumptions['causal'] = True
        result = self.time(**assumptions)
        return self.__class__(result)

    def laplace(self, **assumptions):

        if self.var == s:
            return self        

        result = self.laplace()
        return self.__class__(result)

    def fourier(self, **assumptions):

        if self.var == f:
            return self
        
        assumptions['causal'] = True
        result = self.fourier(**assumptions)
        return self.__class__(result)    

        
class Zgeneric(Generic):

    @classmethod
    def C(cls, Cval):

        return cls(1 / (s * Cval))

    @classmethod
    def G(cls, Gval):

        return cls(1 / Gval)

    @classmethod
    def L(cls, Lval):

        return cls(s * Lval)

    @classmethod
    def R(cls, Rval):

        return cls(Rval)    


class Ygeneric(Generic):

    @classmethod
    def C(cls, Cval):

        return cls(s * Cval)

    @classmethod
    def G(cls, Gval):

        return cls(Gval)

    @classmethod
    def L(cls, Lval):

        return cls(1 / (s * Lval))

    @classmethod
    def R(cls, Rval):

        return cls(1 / Rval)    

class Hgeneric(Generic):
    pass

    
