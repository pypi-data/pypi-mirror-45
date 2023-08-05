import re

class Value(object):
    """Value"""


class Name(object):
    """Name"""


class Lname(object):
    """L Name"""


class Vname(object):
    """V Name"""


class Node(object):
    """Node"""

    def __init__(self, arg):

        if arg.find('.') != -1:
            raise ValueError('Cannot have . in %s name %s' % 
                             (self.__doc__, arg))


class Pnode(Node):
    """Positive node"""


class Nnode(Node):
    """Negative node"""


class Cnnode(Node):
    """Controlling negative node"""


class Cpnode(Node):
    """Controlling positive node"""


class Bnode(Node):
    """Base node"""


class Cnode(Node):
    """Collector node"""


class Enode(Node):
    """Emitter node"""


class Dnode(Node):
    """Drain node"""


class Gnode(Node):
    """Gate node"""


class Snode(Node):
    """Source node"""


def cpt(*args):
    cpts[args[0]] = args[1:]


cpts = {}
cpt('Cname pnode nnode value')
cpt('C', 'Capacitor', Pnode, Nnode, Value)
cpt('D', 'Diode', Pnode, Nnode, ('', 'led', 'shottky', 'tunnel'))
cpt('E', 'VCVS', Pnode, Nnode, Cpnode, Cnnode, Value)
cpt('F', 'VCCS', Pnode, Nnode, Cpnode, Cnnode, Value)
cpt('G', 'CCVS', Pnode, Nnode, Vname, Value)
cpt('H', 'CCSS', Pnode, Nnode, Vname, Value)
cpt('I', 'Current source', Pnode, Nnode, ('', 'ac', 'dc', 'step', 'acstep', 'impulse', 's'), Value)
cpt('J', 'JFET', Dnode, Gnode, Snode, ('njf', 'pjf'))
cpt('K', 'Mutual inductance', Lname, Lname, Value)
cpt('L', 'Inductor', Pnode, Nnode, Value)
cpt('M', 'MOSFET', Dnode, Gnode, Snode, ('nmos', 'pmos'))
cpt('Q', 'Bipolar transistor', Cnode, Bnode, Enode, ('npn', 'pnp'))
cpt('R', 'Resistor', Pnode, Nnode, Value)
cpt('SW', 'Switch', Pnode, Nnode, ('nc', 'no', 'push'))
cpt('V', 'Voltage Source', Pnode, Nnode, ('', 'ac', 'dc', 'step', 'acstep', 'impulse', 's'), Value)


cpt_types = cpts.keys()
cpt_types.sort(lambda x, y: cmp(len(y), len(x)))
cpt_type_pattern = re.compile(r"(%s)([\w']*)" % '|'.join(cpt_types))

    
def parser(string):

    args = re.split(r'[,]*[\s]+', string)

    name = args.pop(0)
    match = cpt_type_pattern.match(name)    

    if not match:
        raise ValueError('Unknown component %s' % name)

    cpt_type = match.groups()[0]
    cpt_id = match.groups()[1]
    print(cpt_type, cpt_id)

    argtypes = cpts[cpt_type]
    print(argtypes)

    kind = argtypes[0]
    
    for argtype in argtypes[1:]:
        if argtype == Value:
            continue
        if not isinstance(argtype, tuple):
            argtype(args)

parser('V 1 2 a3')
parser('V1 1 2 a3')
parser('SWa 1 2')
parser('Q1 1.2 23 4 a3')
