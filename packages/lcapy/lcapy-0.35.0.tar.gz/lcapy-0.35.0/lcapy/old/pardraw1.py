H = (1, 1)

def seps(H):

    N = len(H)
    num_wires = N // 2 * 2

    hcentre = 0
    if N & 1:
        # If N odd, draw cpt without wires
        hcentre = H[N // 2]

    import pdb
    pdb.set_trace()

    # Draw above centre lines
    for n in range(num_wires // 2):

        if n == 0:
            if N & 1:
                sep = H[N // 2] + H[N // 2 - 1]
            else:
                sep = H[N // 2 - 1]
        else:
            sep = H[N // 2 - n] + H[N // 2 - 1 - n]
        sep *= 0.5
        print('%d %s up' % (N // 2 - n - 1, sep))

    # Draw below centre lines
    for n in range(num_wires // 2):

        sep = 0
        if n == 0 and (N & 1):
            sep = H[N // 2]
        sep += H[N // 2 + n]
        sep *= 0.5
        print('%d %s down' % (N // 2 + n, sep))



    
