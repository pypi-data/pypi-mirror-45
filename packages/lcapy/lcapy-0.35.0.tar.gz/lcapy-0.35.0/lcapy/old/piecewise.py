    def _print_Piecewise(self, expr):
        from .symbols import t
        
        if expr.args[0].args[1].has(t >= 0):
            expr = expr.args[0].args[0]
        return super(LcapyPrettyPrinter, self)._print(expr)
    
    def _print_Piecewise(self, expr):
        from .symbols import t
        
        if expr.args[0].args[1].has(t >= 0):
            expr = expr.args[0].args[0]
        return super(LcapyStrPrinter, self)._print(expr)
    

    def _print_Piecewise(self, expr):
        from .symbols import t
        
        if expr.args[0].args[1].has(t >= 0):
            expr = expr.args[0].args[0]
        return super(LcapyLatexPrinter, self)._print(expr)
        
    
