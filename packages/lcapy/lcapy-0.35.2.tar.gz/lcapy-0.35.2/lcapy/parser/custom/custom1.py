import re
import sys
sys.path.append('../..')

import schemcpts as cpts


def anon_cpt_gen():
    count = 1
    while True:
        yield '#%d' % count
        count += 1

anon_cpt_id = anon_cpt_gen()

subcpts = {'V' : (3, ('ac', 'dc', 'sin')),
           'I' : (3, ('ac', 'dc', 'sin')),
           'D' : (3, ('led', 'photo', 'tunnel', 'shottky', 'zener'))}

def parse(string):

    fields = re.split('[ \t\(\),]+', string)

    name = fields[0]
    match = re.match('(SW|TF|TP|[A-Z])(\w+)?', name)
    groups = match.groups()

    cpt, cptid = groups[0], groups[1]
    if cptid is None:
        cptid = anon_cpt_id.next()
        name += cptid

    if cpt in subcpts:
        pos, subtypes = subcpts[cpt]

        if len(fields) > pos and fields[pos].lower() in subtypes:
            cpt += fields[pos].lower()
            fields.pop(pos)
    
    try:
        newclass = getattr(cpts, cpt)
    except:
        newclass = cpts.newclasses[cpt]

    obj = newclass(name, *fields[1:])
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

#v1 = parse('V1 2 3 dc=4')
#print(v1)

v1 = parse('V1 2 3 dc 4')
print(v1)

v2 = parse('V1 2 3 ac 10, 20')
print(v2)

v3 = parse('V1 2 3 sin(0 10 1000)')
print(v3)

v4 = parse('V1 2 3 1.0e3')
print(v4)

v5 = parse('V1 2 3 1e3')
print(v5)

v6 = parse('V 2 3 1e3')
print(v6)

r2 = parse('R1 2 3 {5 * a}')
print(r2)

i3 = parse('I1 2 3 sin(0 10 1000)')
print(i3)
