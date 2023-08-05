from __future__ import print_function
from schemmisc import *
import numpy as np


class Cpt(object):

    pos = {}
    yscale = 1.0
    xscale = 1.0
    cpt_type_counter = 1

    @property
    def num_nodes(self):
        return len(self.pos)

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

    def __init__(self, name, *args, **kwargs):

        self.name = name
        self.args = args
        self.xvals = np.array(self.pos.values())[:, 0]
        self.yvals = np.array(self.pos.values())[:, 1]
                       
        nodes = kwargs['nodes']
        if len(nodes) != len(self.xvals):
            raise ValueError('Expecting %d nodes, got %d' % 
                             (len(self.xvals), len(nodes)))
        self.nodes = nodes

        if hasattr(kwargs, 'opts'):
            opts = kwargs['opts']
        else:
            opts = {}
        if 'dir' not in opts:
            opts['dir'] = None
        if 'size' not in opts:
            opts['size'] = 1

        if opts['dir'] is None:
            opts['dir'] = 'down' if isinstance(self, (Open, Port)) else 'right'
        self.opts = opts

        if hasattr(self, 'check'):
            self.check()


    def draw(self, label_values=True, draw_nodes=True):
        pass


class Q(Cpt):
    """Transistor"""
    
    yscale = 1.5
    xscale = 0.85


    def factory(self, args):

        return {'pnp' : Qpnp,
                'npn' : Qnpn}[args[0]]

    def check(self):

        # For common base, will need to support up and down.
        if self.opts['dir'] not in ('left', 'right'):
            raise ValueError('Cannot draw transistor %s in direction %s'
                             '; try left or right'
                             % (self.name, self.opts['dir']))

    def draw(self, label_values=True, draw_nodes=True):

        n1, n2, n3 = self.nodes
        p1, p2, p3 = self.coords

        centre = Pos(p3.x, 0.5 * (p1.y + p3.y))

        label_str = '$%s$' % self.default_label if label_values else ''
        args_str = '' if self.opts['dir'] == 'right' else 'xscale=-1'
        if 'mirror' in self.opts:
            args_str += ', yscale=-1'
        for key, val in self.opts.iteritems():
            if key in ('color', ):
                args_str += '%s=%s, ' % (key, val)                

        s = r'  \draw (%s) node[%s, %s, scale=%.1f] (T) {};''\n' % (
            centre, tikz_cpt, args_str, self.scale * 2)
        s += r'  \draw (%s) node [] {%s};''\n'% (centre, label_str)

        if tikz_cpt in ('pnp', 'pmos', 'pjfet'):
            n1, n3 = n3, n1

        # Add additional wires.
        if tikz_cpt in ('pnp', 'npn'):
            s += r'  \draw (T.C) -- (%s) (T.B) -- (%s) (T.E) -- (%s);''\n' % (n1, n2, n3)
        else:
            s += r'  \draw (T.D) -- (%s) (T.G) -- (%s) (T.S) -- (%s);''\n' % (n1, n2, n3)


        # s += self._tikz_draw_nodes(self, draw_nodes)
        return s


class Qbipolar(Q):
    """Bipolar transistor"""


class Qpnp(Qbipolar):
    """PNP transistor"""

    tikz_cpt = 'pnp'


class Qnpn(Qbipolar):
    """NPN transistor"""

    tikz_cpt = 'npn'


class Qjfet(Q):
    """JFET"""

    pos = {1: (1, 1), 2: (0, 0.5), 3: (1, 0)}


class Qnjf(Qjfet):
    """N channel JFET"""

    tikz_cpt = 'njf'


class Qpjf(Qjfet):
    """P channel JFET"""

    tikz_cpt = 'pjf'


class Qmos(Qjfet):
    """MOSFET"""


class Qnmos(Qmos):
    """N channel MOSFET"""

    tikz_cpt = 'nmos'


class Qpmos(Qmos):
    """P channel MOSFET"""

    tikz_cpt = 'pmos'


class TwoPort(Cpt):
    """Two-port"""

    pos = {1: (0, 0), 2: (0, 1), 3: (1, 0), 4: (1, 1)}


class TF(TwoPort):
    """Transformer"""


class OnePort(Cpt):
    """OnePort"""

    # horiz, need to rotate for up/down
    pos = {1: (0, 0), 2: (1, 0)}


class R(OnePort):
    """R"""


class C(OnePort):
    """C"""


class L(OnePort):
    """L"""


class Open(OnePort):
    """Open circuit"""

    # vert, need to rotate for left/right
    pos = {1: (0, 0), 2: (0, 1)}


class Port(Open):
    """Port circuit"""


class CS(Cpt):
    """Controlled source"""


class VCVS(CS):
    """VCVS"""


class VCCS(CS):
    """VCCS"""


class CCVS(CS):
    """CCVS"""


class CCCS(CS):
    """CCCS"""


class K(Cpt):
    """K"""


cpt_map = {'R': R, 'C': C, 'L': L, 'Z': OnePort , 'Y': OnePort, 
           'V': OnePort, 'I': OnePort, 'W': Wire, 'O': Open, 'P': Port,
           'E': VCVS, 'F': CCVS, 'G': VCCS, 'H': CCCS, 'D': Diode,
           'J': Jfet, 'M': MOSfet, 'Q': , 'SW': Switch, 'TF': TF,
           'TP': TP, 'K': K}

cpt_types = cpt_map.keys()

# Regular expression alternate matches stop with first match so need
# to have longer names first.
cpt_types.sort(lambda x, y: cmp(len(y), len(x)))

cpt_type_pattern = re.compile(r"(%s)([\w']*)" % '|'.join(cpt_types))

def cpt_make(name, n1, n2, *args, **opts):

    match = cpt_type_pattern.match(name)

    if not match:
        raise ValueError('Unknown schematic component %s' % name)

    # Circuitikz does not like a . in a name
    if n1.find('.') != -1:
        raise ValueError('Cannot have . in node name %s' % n1)
    if n2.find('.') != -1:
        raise ValueError('Cannot have . in node name %s' % n2)

    cpt_type = match.groups()[0]
    cpt_id = match.groups()[1]

    if cpt_id is None:
        Cpt.cpt_type_counter += 1
        name = cpt_type + '#%d' % Cpt.cpt_type_counter
        
    # There are two possible labels for a component:
    # 1. Component identifier, e.g., R1
    # 2. Component value, expression, or symbol
    id_label = tex_name(cpt_type, cpt_id)
    value_label = None

    # TODO: Map cpt_type to class
    cpt = cpt_map[cpt_type]

    # But what about subtype, say JFET transistors?
    if hasattr(cpt, 'factory'):
        cpt = cpt.factory(args)

    return cpt



q = Qjfet('Q1', nodes=('3', '4', '5'))
print('xmin %d xmax %d xextent %d' % (q.xmin, q.xmax, q.xextent))
print('ymin %d ymax %d yextent %d' % (q.ymin, q.ymax, q.yextent))
#print(q.draw())
