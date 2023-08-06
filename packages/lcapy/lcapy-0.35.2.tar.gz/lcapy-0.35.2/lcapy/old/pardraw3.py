    def net_make(self, net, n1=None, n2=None):

        s = []
        if n1 is None:
            n1 = net.node
        n3, n4 =  net.node, net.node

        H = [arg.height * 0.5 for arg in self.args]
        
        N = len(H)
        num_wires = N // 2 * 2

        # Draw component in centre if have odd number in parallel.
        if (N & 1):
            s.append(self.args[N // 2].net_make(net, n3, n4))

        na, nb = n3, n4

        s.append('W %s %s; right, size=%s' % (n1, n3, self.wsep))

        # Draw components above centre
        for n in range(num_wires // 2):

            if not (N & 1) and n == 0:
                sep = H[N // 2 - 1]
            else:
                sep = H[N // 2 - n] + H[N // 2 - 1 - n]

            sep += self.hsep
            nc, nd =  net.node, net.node
            s.append('W %s %s; up, size=%s' % (na, nc, sep))
            s.append('W %s %s; up, size=%s' % (nb, nd, sep))
            s.append(self.args[N // 2 - n].net_make(net, nc, nd))
            na, nb = nc, nd

        na, nb = n3, n4

        # Draw components below centre
        for n in range(num_wires // 2):

            if not (N & 1) and n == 0:
                sep = H[N // 2]
            else:
                sep = H[N // 2 + n] + H[N // 2 - 1 + n]

            sep += self.hsep
            nc, nd =  net.node, net.node
            s.append('W %s %s; down, size=%s' % (na, nc, sep))
            s.append('W %s %s; down, size=%s' % (nb, nd, sep))
            s.append(self.args[N // 2 + n].net_make(net, nc, nd))
            na, nb = nc, nd

        if n2 is None:
            n2 = net.node

        s.append('W %s %s; right, size=%s' % (n4, n2, self.wsep))
        return '\n'.join(s)
