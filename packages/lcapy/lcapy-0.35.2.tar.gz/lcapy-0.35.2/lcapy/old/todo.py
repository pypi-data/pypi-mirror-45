if args != () and cpt_type in ('V', 'I'):
            # If have a t-domain expression, use v and i.
            expr = Expr(args[0], cache=False)
            if expr.expr.find(tsym) != set():
                cpt_type = 'v' if cpt_type == 'V' else 'i'


        if len(args) == 0:
            # Ensure symbol uppercase for s-domain value.
            if cpt_type in ('Vdc', 'Vac', 'Idc', 'Iac'):
                value = uppercase_name(value)

            args = (value, )





    @property
    def i(self):
        """Time-domain current through element"""

        return self.cct._i[self.name]

    @property
    def V(self):
        """Voltage drop across element"""

        return self.cct._V[self.name]

    @property
    def v(self):
        """Time-domain voltage drop across element"""

        return self.cct._v[self.name]

    @property
    def Y(self):
        """Admittance"""
        
        return self.cpt.Y

    @property
    def Z(self):
        """Impedance"""
        
        return self.cpt.Z


    def __str__(self):

        def quote(arg):
            if arg.find('(') != -1:
                return '{%s}' % arg
            if arg.find(' ') != -1:
                return '"%s"' % arg
            return arg

        args = (self.name, ) + self.nodes[0:2] + self.args
        return ' '.join(['%s' % quote(arg) for arg in args])




        net = fields[0].strip()
        if net[-1] == '"':
            quote_pos = net[:-1].rfind('"')
            if quote_pos == -1:
                raise ValueError('Missing " in net: ' + net)
            args = (net[quote_pos + 1:-1], ) + args
            net = net[:quote_pos - 1]


        if string[0] == ';':
            keypairs = string[1:].split(',')
            for keypair in keypairs:
                fields = keypair.split('=')
                key = fields[0].strip()
                arg = fields[1].strip() if len(fields) > 1 else ''
                if arg.lower() == 'false':
                    arg = False
                elif arg.lower() == 'true':
                    arg = True
                self.opts[key] = arg
            return


implicitly linked nodes 0_1 0_2 etc?

        n1, n2 = elt.nodes[0:2]

        if elt.cpt_type != 'W' and (
                Node(self, n1).rootname == Node(self, n2).rootname):
            raise ValueError('Component %s shorted by implicitly linked nodes %s and %s' % (elt.name, n1, n2))


anonymous Open 
1. parser create name
2. open create name


Open(nodes=(n1, n2), opts) -> create O#1 n1 n2; opts

Cpt(name=???, )


    def __str__(self):

        def quote(arg):
            # TODO: If any delimiter put arg in {}
            if arg.find('(') != -1:
                return '{%s}' % arg
            if arg.find(' ') != -1:
                return '"%s"' % arg
            return arg

        args = (self.name, ) + self.nodes[0:2] + self.args
        return ' '.join(['%s' % quote(arg) for arg in args])





    def _model(self, var=None):

        cct = Circuit()
        cct.opts = copy(self.opts)
        cct._s_model = True

        for key, elt in self.elements.iteritems():

            cpt_type = elt.type

            elif cpt_type in ('V', 'Vdc', 'Vac', 'Vimpulse',
                              'Vstep', 'Vacstep'):
                new_elt = self._make_V(
                    elt.nodes[0], elt.nodes[1], elt.cpt.V(var), elt.opts)
            elif cpt_type in ('I', 'Idc', 'Iac', 'Iimpulse',
                              'Istep', 'Iacstep'):
                new_elt = self._make_I(
                    elt.nodes[0], elt.nodes[1], elt.cpt.I(var), elt.opts)
            else:
                new_elt = copy(elt)
                new_elt.cct = cct

            if cpt_type in ('C', 'L', 'R') and elt.cpt.V != 0:


            # Make voltage and current labels uppercase.
            for opt, val in new_elt.opts.strip_voltage_labels().iteritems():
                new_elt.opts[opt] = uppercase_name(val)
            for opt, val in new_elt.opts.strip_current_labels().iteritems():
                new_elt.opts[opt] = uppercase_name(val)
            cct._elt_add(new_elt)

        return cct


    def _make_node(self):
        """Create a dummy node"""

        if not hasattr(self, '_node_counter'):
            self._node_counter = 0
        self._node_counter += 1
        return '_%d' % self._node_counter


# Can't tell the following... need to solve cct first

    @property
    def v0(self):
        """Pre-initial voltage drop across component"""

        try:
            return self.cpt.v0
        except:
            return 0.0

    @property
    def i0(self):
        """Pre-initial current through component"""

        try:
            return self.cpt.i0
        except:
            return 0.0


