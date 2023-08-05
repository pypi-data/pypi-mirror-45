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


cpt_type_pattern = re.compile(r"([A-Z]*)name")

def cpt(string):

    match = cpt_type_pattern.match(string)    
    cpt_type = match.groups()[0]

    cpts[cpt_type] = string

cpts = {}
cpt('Cname NP NM Value <IC=Value>')
cpt('Lname NP NM Value <IC=Value>')
cpt('Rname NP NM Value')
# So how do we choose the correct rule without going down the path of
# using a lex/yacc based parser with the inherently bad error
# messages?  And how do we tell a keyword such as ac, dc, sin, etc.
# from a symbolic node name?
cpt('Vname NP NM <DC=> Value')
cpt('Vname NP NM AC Value, Phase')
cpt('Vname NP NM SIN(VO, VA, fo <TD> <a> <phase>)')



cpt_types = cpts.keys()
cpt_types.sort(lambda x, y: cmp(len(y), len(x)))
cpt_type_id_pattern = re.compile(r"(%s)([\w']*)" % '|'.join(cpt_types))

    
def parser(string):

    match = cpt_type_id_pattern.match(string)    

    if not match:
        raise ValueError('Unknown component %s' % string)

    cpt_type = match.groups()[0]
    cpt_id = match.groups()[1]

    argfmt = cpts[cpt_type]

    args = {}
    while argfmt:
        print(argfmt, string)
        if argfmt[0] == '<':
            foo, argfmt = argfmt.split('>', 1)
            print('Opt', foo)
            argfmt = argfmt.strip()
            continue
 
        if ' ' in argfmt:
            argname, argfmt = argfmt.split(' ', 1)
            arg, string = string.split(' ', 1)
            string = string.strip()
        else:
            argname, argfmt = argfmt, ''
            arg = string

        args[argname] = arg

    print(args)


parser('V 1 2 a3')
parser('V1 1 2 a3')
parser('V1 1 2 3 * 5')
#parser('SWa 1 2')
#parser('Q1 1.2 23 4 a3')
