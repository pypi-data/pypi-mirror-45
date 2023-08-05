def test():
    symbols = {}
    s1 = sympify1('5 * E1 + a', symbols)
    s2 = sympify1('5 * R1 + a', symbols, real=True)
    print(symbols['R_1'].assumptions0)
    s3 = sympify1('5 * R1 + a', symbols, positive=True)
    print(symbols1['R_1'].assumptions0)

