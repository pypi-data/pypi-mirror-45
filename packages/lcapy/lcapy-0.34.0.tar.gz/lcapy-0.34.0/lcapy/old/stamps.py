    def _I_stamp(self, elt):
        """Add stamp for current source (independent and dependent)"""

        n1 = cct._node_index(self.nodes[0])
        n2 = cct._node_index(self.nodes[1])

        if isinstance(self.cpt, VCCS):
            n3 = cct._node_index(self.nodes[2])
            n4 = cct._node_index(self.nodes[3])


        elif isinstance(self.cpt, CCCS):



        else:

