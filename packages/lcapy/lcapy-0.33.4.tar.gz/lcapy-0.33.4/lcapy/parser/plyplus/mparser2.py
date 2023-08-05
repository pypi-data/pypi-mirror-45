from plyplus import Grammar, ParseError
from grammar2 import grammar
import schemcpts as cpts

parser = Grammar(grammar)


def parse(string):
    
    try:
        thing = parser.parse(string)
    except ParseError as e:
        raise ParseError('Could not parse: %s: due to %s' % (string, e))
        
    classname = str(thing.tail[0].head).capitalize()
    name = str(thing.tail[0].tail[0].tail[0])

    try:
        newclass = getattr(cpts, classname)
    except:
        newclass = cpts.newclasses[classname]

    obj = newclass(name)

    # Add attributes.
    obj.nodes = ()
    for field in thing.tail[0].tail[1:]:
        attr, val = field.head, field.tail[0] 
        if 'node' in attr:
            obj.nodes += (val, )
        setattr(obj, attr, val)

    obj.string = string


    return obj


r = parse('R1 2 3 4')
print(r)

r1 = parse('R1 2 3')
print(r1)

q = parse('Q1 2 3 4 pnp')
print(q)

j = parse('Ja2 2 3 4 pjf')
print(j)

s = parse('SW1 2 3 push')
print(s)

d1 = parse('D1 2 3 led')
print(d1)

v1 = parse('V1 2 3')
print(v1)

v1 = parse('V1 2 3 dc=4')
print(v1)

v2 = parse('V1 2 3 ac 10, 20')
print(v2)

v3 = parse('V1 2 3 sin(0 10 1000)')
print(v3)

v4 = parse('V1 2 3 1.0e3')
print(v4)

v5 = parse('V1 2 3 1e3')
print(v5)

r2 = parse('R1 2 3 {5 * a}')
print(r2)

i3 = parse('I1 2 3 sin(0 10 1000)')
print(i3)

e1 = parse('E1 2 3 4 5 1e3')
print(e1)

r2 = parse('Rin 1 2 3')
print(r2)

r3 = parse('R 1 2 3')
print(r3)
