class Cnodes(dict):
    """Common nodes"""

    def __init__(self, nodes):

        super (Cnodes, self).__init__()
        for node in nodes:
            self[node] = (node, )

    def link(self, n1, n2):
        """Make nodes n1 and n2 share common node"""

        set1 = self[n1]
        set2 = self[n2]
        newset = set1 + set2

        for n in self[n1]:
            self[n] = newset
        for n in self[n2]:
            self[n] = newset



nodes = ('1', '2', '3', '4', '5', '6')


cnodes = Cnodes(nodes)
cnodes.link('2', '3')
cnodes.link('6', '5')
cnodes.link('6', '2')
