class Assumptions(dict):

    known = 'ac', 'dc', 'causal'

    @property
    def ac(self):
        return self.get('ac', False)

    @property
    def dc(self):
        return self.get('dc', False)

    @property
    def causal(self):
        return self.get('causal', False)

    def check(self):

        if self.ac and self.dc:
            raise ValueError('Incompatible assumptions ac and dc')

        if self.ac and self.causal:
            raise ValueError('Incompatible assumptions ac and causal')

        if self.dc and self.causal:
            raise ValueError('Incompatible assumptions dc and causal')        

    def add(self, **assumptions):
        
        self.update(assumptions)
        self.check(assumptions)

    def override(self, **assumptions):

        if assumptions == {}:
            return
        
        for assumption in self.known:
            self.pop(assumption)

        self.add(assumptions)



    @property
    def assumptions(self):
        
        assumptions = {}
        for attr in 'ac', 'dc', 'causal':
            if hasattr(self, attr):
                assumptions[attr] = getattr(self, attr)
        return assumptions


    @property
    def assumptions(self):
        
        assumptions = {}
        for attr in 'ac', 'dc', 'causal':
            if hasattr(self, attr):
                assumptions[attr] = getattr(self, attr)
        return assumptions

