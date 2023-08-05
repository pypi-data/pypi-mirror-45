from lcapy.core import sExpr

class Superposition(object):

    def __init__(self, val=None):
        self.args = []
        if val is not None:
            self.args.append(val)

    @property
    def expr(self):

        result = 0
        for term in self.args:
            result += term.laplace().expr
        return result

    def __add__(self, x):
        """Add"""

        new = Superposition()
        for x1 in self.args:
            new.args.append(x1)
        new.args.append(x)
        return new

    def time(self, **assumptions):
        
        result = 0
        for term in self.args:
            result += term.time(**assumptions)
        return result

    def phasor(self, **assumptions):
        
        result = 0
        for term in self.args:
            result += term.phasor(**assumptions)
        return result

    def laplace(self, **assumptions):
        
        result = 0
        for term in self.args:
            result += term.laplace(**assumptions)
        return result


# result.v
# result.V
# result.Vac 
# result.i
# result.I
# result.Iac
#
# cct.R1.Vac
# cct[1].Vac
#
# BranchResult()  .i .I .Iac .v .V .Vac
# NodeResult()    .v .V .Vac



class Vresult(Superposition):

    def v(self):
        return self.time()

    def V(self):
        return self.laplace()

    def Vac(self):
        return self.phasor()


class Iresult(Superposition):

    def i(self):
        return self.time()

    def I(self):
        return self.laplace()

    def Iac(self):
        return self.phasor()
