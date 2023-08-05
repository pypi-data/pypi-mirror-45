def laplace_match(expr, t, s):

    # Strategies:
    # 1. ad-hoc
    # 2. table matching
    # 3. decision tree
    
    n = sym.symbols('n', integer=True)
    a = sym.symbols('a', real=True)
    t = sym.symbols('t', real=True)
    tau = sym.symbols('tau', real=True)
    s = sym.symbols('s')
    f = sym.Function('f')
    g = sym.Function('g')
    F = sym.Function('F')
    G = sym.Function('G')        
    
    transforms = {t**n * f(t): (-1)**n * sym.diff(F(s), (s, n)),
                  sym.Integral(f(tau), (tau, 0, t)): F(s) / s}


    funcs = []
    factors = expr.as_ordered_factors()    
    for factor in factors:
        if isinstance(factor, sym.function.AppliedUndef):
            funcs.append(factor)

    def match_factors(matchfactors):

        for factor1, factor2 in zip(factors, matchfactors):
            if not isinstance(factor2, factor1.__class__):
                return False
        return True
            
    for match, transform in transforms.items():
        matchfactors = match.as_ordered_factors()
        if len(matchfactors) != len(factors):
            continue
        if match_factors(matchfactors):
            print(matchfactors)
            break
            

