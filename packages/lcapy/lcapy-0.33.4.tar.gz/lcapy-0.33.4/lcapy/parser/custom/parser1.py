import re

subcpts = {
    'D' : (3, ('led', 'photo', 'tunnel', 'shottky', 'zener'))
    'I' : (3, ('ac', 'dc', 'sin')),
    'J' : (4, ('pjf', 'njf')),
    'M' : (4, ('nmos', 'pmos')),
    'Q' : (4, ('pnp', 'npn')),
    'SW' : (3, ('no', 'nc', 'push')),
    'V' : (3, ('ac', 'dc', 'sin'))
}

cpt_pattern = re.compile('(SW|TF|TP|[A-Z])(\w+)?')
split_pattern = re.compile('[ \t\(\),]+')

class Parser(object):

    def __init__(self, cpts):

        self.cpts = cpts
        self._anon_count = 0
    
    def _anon_cpt_id(self):

        self._anon_count += 1
        return '#%d' % self._anon_count

    def parse(self, string):
        """Parse string and create object"""

        fields = string.split(';')
        opts_string = fields[1].strip() if len(fields) > 1 else ''

        fields = split_pattern.split(fields[0])
        
        name = fields[0]
        match = cpt_pattern.match(name)
        groups = match.groups()
        
        # Add id if anonymous.
        cpt, cptid = groups[0], groups[1]
        if cptid is None:
            name += self._anon_cpt_id()

        # Create object.
        if cpt in subcpts:
            pos, subtypes = subcpts[cpt]

            if len(fields) > pos and fields[pos].lower() in subtypes:
                cpt += fields[pos].lower()
                fields.pop(pos)
    
        try:
            newclass = getattr(self.cpts, cpt)
        except:
            newclass = self.cpts.newclasses[cpt]

        obj = newclass(name, *fields[1:])
        obj.string = string
        obj.opts_string = opts_string

        return obj


