class Cpt(object):

    num_nodes = 2
    sub_types = ()

    def __init__(self, name, *args, **kwargs):

        self.sub_type = None

        if sub_types != ():
            if len(args) == 0:
                self.sub_type = sub_types[0]
            else:
                self.sub_type = arg[0]                
                if self.sub_type not in sub_types:
                    raise ValueError('Unknown subtype %s for %s' % (self.sub_type, name))

        pass


class Q(Cpt):
    """Transistor"""
    
    num_nodes = 3
    sub_types = ('npn', 'pnp')
    yscale = 1.5
    xscale = 0.85


class J(Q):
    """JFET"""

    sub_types = ('njf', 'pjf')


    def xplace(self, graphs, size=1):

        graphs.add(m2, m1, xscale * size)        

    def yplace(self, graphs, size=1):

        if self.sub_type == 'pjf':
            graphs.add(m3, m2, yscale * size * 0.68)
            graphs.add(m2, m1, yscale * size * 0.32)
        else:
            graphs.add(m3, m2, yscale * size * 0.32)
            graphs.add(m2, m1, yscale * size * 0.68)


class M(Q):
    """MOSFET"""

    sub_types = ('nmos', 'pmos')
    xscale = 1.0

    
# component('M', Q, ('nmos', 'pmos'))

