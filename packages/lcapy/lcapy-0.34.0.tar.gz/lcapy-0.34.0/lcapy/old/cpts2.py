class Cpt(object):

    num_nodes = 2
    sub_types = ()
    dims = {}

    def __init__(self, name, *args, **kwargs):

        self.sub_type = None

        if sub_types != ():
            if len(args) == 0:
                self.sub_type = sub_types[0]
            else:
                self.sub_type = arg[0]                
                if self.sub_type not in sub_types:
                    raise ValueError('Unknown subtype %s for %s' % (self.sub_type, name))


    def xplace(self, graphs, nodes, size=1):

        for dim, value in dims.iter_values():
            
            dir, n1, n2 = dim
            if dir != 'x':
                continue
            graphs.add(nodes[int(n1) - 1], nodes[int(n2) - 1], xscale * size * value)

    def yplace(self, graphs, nodes, size=1):

        for dim, value in dims.iter_values():
            
            dir, n1, n2 = dim
            if dir != 'y':
                continue
            graphs.add(nodes[int(n1) - 1], nodes[int(n2) - 1], yscale * size * value)
                       

class Q(Cpt):
    """Transistor"""
    
    num_nodes = 3
    yscale = 1.5
    xscale = 0.85


class Qbipolar(Q):


class Qpnp(Qbipolar):
    """PNP transistor"""


class Qnpn(Qbipolar):
    """NPN transistor"""


class Qjfet(Q):
    """MOSFET"""

    dims = {'x21': 1, 'y32': 0.5, 'y21': 0.5}
    pos = {1: (1, 1), 2: (0, 0.5), 3: (1, 0)}


class Qnjf(Qjfet):
    """N channel JFET"""




class Qpjf(Qjfet):
    """P channel JFET"""


class Qmos(Q):
    """MOSFET"""


class Qnmos(Qmos):
    """N channel MOSFET"""


class Qpmos(Qmos):
    """P channel MOSFET"""


