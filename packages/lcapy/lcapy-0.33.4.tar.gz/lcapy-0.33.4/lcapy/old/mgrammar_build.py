import re
from grammar import elements, args, whitespace

class Arg(object):

    def __init__(self, name, base, comment):
        
        self.name = name
        self.base = base
        self.comment = comment
        self.baseclass = None

    def is_opt(self):

        return self.name[0] == '['

    def is_valid(self, string):

        if self.baseclass is None:
            return True
        return self.baseclass.is_valid(string)


class Element(object):

    def __init__(self, name, args, comment):
        
        self.name = name
        self.args = args
        self.comment = comment


class Parser(object):

    def __init__(self, elements, args, whitespace=' '):

        self.args = {}
        self.elements = {}
        
        args = args.split('\n')
        for arg in args:
            self.add_arg(arg)

        elements = elements.split('\n')
        for element in elements:
            self.add_element(element)

        cpts = self.elements.keys()
        cpts.sort(key=len, reverse=True)

        self.cpt_pattern = re.compile('(%s)(\w+)?' % '|'.join(cpts))
        self.split_pattern = re.compile(whitespace)


    def add_arg(self, string):

        if string == '':
            return

        fields = string.split(':')
        argname = fields[0]
        fields = fields[1].split(';')
        argbase = fields[0].strip()
        comment = fields[1].strip()
        
        print(argname, argbase, comment)
        self.args[argname] = Arg(argname, argbase, comment)

    def add_element(self, string):

        if string == '':
            return

        fields = string.split(':')
        eltcname = fields[0]
        fields = fields[1].split(';')
        string = fields[0].strip()
        comment = fields[1].strip()
        
        fields = string.split(' ')
        args = fields[1:]

        eltname = fields[0][0:-4]
        
        for arg in args:
            if arg[0] == '[':
                arg = arg[1:-1]
            if arg not in self.args:
                print('Unknown argument %s for %s' % (arg, string))

        if eltname not in self.elements:
            self.elements[eltname] = ()
        self.elements[eltname] += (Element(eltcname, args, comment), )

        print(fields, comment)

        def _anon_cpt_id(self):

            self._anon_count += 1
            return '#%d' % self._anon_count

    def parse(self, string):
        """Parse string and create object"""

        fields = string.split(';')
        opts_string = fields[1].strip() if len(fields) > 1 else ''

        fields = self.split_pattern.split(fields[0])
        
        name = fields[0]
        match = self.cpt_pattern.match(name)
        groups = match.groups()
        
        # Add id if anonymous.
        cpt, cptid = groups[0], groups[1]
        if cptid is None:
            name += self._anon_cpt_id()



        # # Create object.
        # if cpt in subcpts:
        #     pos, subtypes = subcpts[cpt]

        #     if len(fields) > pos and fields[pos].lower() in subtypes:
        #         cpt += fields[pos].lower()
        #         fields.pop(pos)
    
        # try:
        #     newclass = getattr(self.cpts, cpt)
        # except:
        #     newclass = self.cpts.classes[cpt]

        # obj = newclass(name, *fields[1:])
        # obj.string = string
        # obj.opts_string = opts_string

        #return obj




parser = Parser(elements, args, whitespace)
